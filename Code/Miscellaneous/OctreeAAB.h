#pragma once

#include <vector>
#include <stack>
#include "math3d.h"
#include "Triangle.h"

class OctreeNode 
{
	public:
		vec3 min, max; 
		vec3 color;
		//min max (x,y,z) value (boudning box)
		std::vector<unsigned> children = std::vector<unsigned>(8);
		std::vector<Triangle> triangles = std::vector<Triangle>(); //only used for leaf
		std::array<vec4,6> planes = std::array<vec4, 6>();//six planes of this node
		std::array<vec3, 6> pointsOnPlane = std::array<vec3, 6>();
		static std::vector<OctreeNode> nodes;    //all nodes
		const unsigned int MAXDEPTH = 8, MAXTRIS = 1;
		//max height of tree & max num of tris allowed per child (if possible)
		vec3 depth_width_height;
		std::array<vec3, 8> vertecies = std::array<vec3, 8>();

		bool contains(const Triangle& T) 
		{ 

			//ERROR: T.p[i] is sometimes garbage, ie unitiallizted "unable to read memory"

			int i;
			for (i = 0; i<3; ++i) 
			{ 
				if (pointInBox(T.p[i]))
					return true; 
			}

			for (i = 0; i<3; ++i) 
			{ 
				if (segmentBoxIntersection(T.p[i], T.p[(i + 1) % 3]))
					return true; 
			}

			if (segmentTriangleIntersection(vertecies.at(0), vertecies.at(4), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(0), vertecies.at(1), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(0), vertecies.at(2), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(5), vertecies.at(4), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(6), vertecies.at(4), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(1), vertecies.at(5), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(1), vertecies.at(3), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(2), vertecies.at(3), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(6), vertecies.at(7), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(7), vertecies.at(5), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(7), vertecies.at(3), T))
				return true;
			if (segmentTriangleIntersection(vertecies.at(0), vertecies.at(4), T))
				return true;
			return false; 
		}

		bool pointInBox(const vec3 & point)
		{
			float lx, ly, lz;
			vec3 Q;
			
			Q = point - (depth_width_height/2.0f);
			lx = dot(Q, vec3(1, 0, 0));
			ly = dot(Q, vec3(0, 1, 0));
			lz = dot(Q, vec3(0, 0, 1));
			if (lx >= -depth_width_height.x && lx <= depth_width_height.x && 
				ly >= -depth_width_height.y && ly <= depth_width_height.y && 
				lz >= -depth_width_height.z && lz <= depth_width_height.z)
				return true;
			
			return false;
		}

		bool segmentBoxIntersection(const vec3 & point1, const vec3 & point2)
		{
			for(int i = 0; i < 6; i++)
			{
				vec4 plane = planes[i];
				vec3 point = pointsOnPlane[i];
				vec3 t = vec3{ plane.x, plane.y, plane.z };
				if (rayPlaneIntersection(t, plane.w, point, point1, point2) >= 0)
				{
					return true;
				}
			}
			return false;
			
		}

		bool segmentTriangleIntersection(const vec3 & v, const vec3 & s, const Triangle & T)
		{
			float denum = dot(T.N, v);
			if (denum == 0)
			{
				//parallel
				return false;
			}

			float t1 = -1 * (T.D + dot(T.N, s)) / denum;
			if (t1 < 0)
			{
				//no intersection
				return false;
			}
			vec3 ips = s + (t1*v);
			float area = 0;
			//abp, apc, pcb
			for (int i = 0; i < 3; i++)
			{
				vec3 p = T.p[i];
				vec3 q = cross(T.e[i], (ips - p));
				area += q.magnitude();
			}

			if (area*T.oneOverTwiceArea <= 1.001)
			{
				return true;
			}

			return false;
		}

		float rayPlaneIntersection(const vec3& normal, const float planeDistance, const vec3& pointOnPlane, const vec3& rayStart, const vec3& rayDirection)
		{
			float denom = dot(normal, rayDirection);
			//if denom is zero, we get t=infinity
			float number = -(planeDistance + dot(normal,rayStart) );
			float t = number/denom;
			return t;
		}

		void planePairIntersection(const vec4& p1, const vec3& v1, const vec4& p2, const vec3& v2, const vec3&s, const vec3& v, float& t1, float& t2)
		{ 
			vec3 t = vec3{ p1.x, p1.y, p1.z};
			t1 = rayPlaneIntersection(t, p1.w, v1, s, v); 
			t = vec3{ p2.x, p2.y, p2.z };
			t2 = rayPlaneIntersection(t, p2.w, v2, s, v);
			if (t1 > t2) 
			{ 
				float tmp = t1; 
				t1 = t2; 
				t2 = tmp; 
			} 
		}

		bool rayBoxIntersection(const std::array<vec4,6>& planes, const vec3& s, const vec3& v )
		{
			//intersection b/w an axis aligned plane & a ray is just y = mx + b, or RayDirection * t + RayOrigin
			//equation for the plane is a constant line @ that x, y , or z value. example: min x = 1
			//so the quation is x = 1.
			//t.x = (plane - RayOrigin.x) / RayDirection.x
			float txmin = (min.x - s.x) / v.x;
			float txmax = (max.x - s.x) / v.x;

			if (txmin > txmax) std::swap(txmin, txmax);

			float tymin = (min.y - s.y) / v.y;
			float tymax = (max.y - s.y) / v.y;

			if (tymin > tymax) std::swap(tymin, tymax);

			if ((txmin > tymax) || (tymin > txmax))
				return false;
			//(tmin > tymax) -> intersects the min.x and max.x planes before it hits the y planes
			//it misses the box ( / [] )
			//(tymin > tmax) -> it misses the box and intersets the min.y and max.y past the box
			//( [] /)

			if (tymin > txmin)
				txmin = tymin;

			if (tymax < txmax)
				txmax = tymax;

			float tzmin = (min.z - s.z) / v.z;
			float tzmax = (max.z - s.z) / v.z;

			if (tzmin > tzmax) std::swap(tzmin, tzmax);

			if ((txmin > tzmax) || (tzmin > txmax))
				return false;
			//(tmin > tzmax) -> intersects the min.x and max.x planes before it hits the z planes
			//it misses the box ( / [] ) and goes above
			//(tzmin > tmax) -> it misses the box and intersets the min.z and max.z bellow the box
			//( [] /)

			if (tzmin > txmin)
				txmin = tzmin;

			if (tzmax < txmax)
				txmax = tzmax;

			return true;
		}

		void setMinMax(const vec3 & minimum, const vec3 & maximum)
		{
			min = minimum;
			max = maximum;
			depth_width_height = (max - min);
			if (depth_width_height.x < 0)
				depth_width_height.x *= -1;
			if (depth_width_height.y < 0)
				depth_width_height.y *= -1;
			if (depth_width_height.z < 0)
				depth_width_height.z *= -1;

			setPlanesAndVertecies(min, max);
		}

		OctreeNode(const vec3 & minimum, const vec3 & maximum)
		{
			//min and max are calculated by beforehand per mesh.
			//DOES NOT WORK WITH MOTION, these values are stored away not calcuated every time
			vec3 min;
			min.x = std::min(minimum.x, maximum.x);
			min.y = std::min(minimum.y, maximum.y);
			min.z = std::min(minimum.z, maximum.z);
			vec3 max;
			max.x = std::max(minimum.x, maximum.x);
			max.y = std::max(minimum.y, maximum.y);
			max.z = std::max(minimum.z, maximum.z);
			setMinMax(min, max);
		}

		void setPlanesAndVertecies(const vec3 & min, const vec3 & max)
		{
			vec3 v1, v2, cp, A, B, C, D, E, F, G, H;
			float d;

			A = vec3(min.x, max.y, min.z);
			B = vec3(max.x, max.y, min.z);
			C = min;
			D = vec3(max.x, min.y, min.z);
			E = vec3(min.x, max.y, max.z);
			F = max;
			G = vec3(min.x, min.y, max.z);
			H = vec3(max.x, min.y, max.z);

			vertecies[0] = A;
			vertecies[1] = B;
			vertecies[2] = C;
			vertecies[3] = D;
			vertecies[4] = E;
			vertecies[5] = F;
			vertecies[6] = G;
			vertecies[7] = H;

			//0
			v1 = B-A;
			v2 = B-C;
			cp = normalize(cross(v1, v2));
			d = dot(B, cp);
			planes[0] = vec4{ cp.x, cp.y, cp.z, d };
			pointsOnPlane[0] = A;

			//1
			v1 = E-A;
			v2 = E-C;
			cp = normalize(cross(v1, v2));
			d = dot(A, cp);
			planes[1] = vec4{ cp.x, cp.y, cp.z, d };
			pointsOnPlane[1] = A;

			//2
			v1 = F-E;
			v2 = F-G;
			cp = normalize(cross(v1, v2));
			d = dot(F, cp);
			planes[2] = vec4{ cp.x, cp.y, cp.z, d };
			pointsOnPlane[2] = E;

			//3
			v1 = G-C;
			v2 = G-D;
			cp = normalize(cross(v1, v2));
			d = dot(G, cp);
			planes[3] = vec4{ cp.x, cp.y, cp.z, d };
			pointsOnPlane[3] = C;

			//4
			v1 = B-A;
			v2 = B-E;
			cp = normalize(cross(v1, v2));
			d = dot(B, cp);
			planes[4] = vec4{ cp.x, cp.y, cp.z, d };
			pointsOnPlane[4] = A;

			//5
			v1 = B-D;
			v2 = B-F;
			cp = normalize(cross(v1, v2));
			d = dot(B, cp);
			planes[5] = vec4{ cp.x, cp.y, cp.z, d };
			pointsOnPlane[5] = B;

			//for (int i = 0; i < 6; i++)
			//	std::cout << planes[i] << std::endl;
		}

		void initialize(int depth, std::vector<Triangle>& tris)
		{
			int idx = 0;
			if (depth >= MAXDEPTH || tris.size() <= MAXTRIS)
			{
				nodes.at(idx).children.clear();
			}
			else
			{
				idx = nodes.size();
				//add 8 child to nodes[]

				vec3 ourMin, ourMax;
				vec3 center = min + depth_width_height / 2.0f;
				OctreeNode* node;

				vec3 boundsOffsetTable[8] =
				{
						{-0.5, -0.5, -0.5},
						{+0.5, -0.5, -0.5},
						{-0.5, +0.5, -0.5},
						{+0.5, +0.5, -0.5},
						{-0.5, -0.5, +0.5},
						{+0.5, -0.5, +0.5},
						{-0.5, +0.5, +0.5},
						{+0.5, +0.5, +0.5}
				};

				for (int i = 0; i < 8; i++)
				{
					ourMin = center;
					ourMax = center - boundsOffsetTable[i]* depth_width_height;
					auto node = OctreeNode(ourMin, ourMax);
					node.color = color;
					nodes.push_back(node);
					node.children.at(i) = idx + i;
					//add children
				}
				

				//do stuff here
				for (Triangle& T : tris)
				{
					for (int j = 0; j < 8; ++j)
					{
						if (nodes.at(idx + j).contains(T))
						{
							nodes.at(idx + j).triangles.push_back(T);
						}
					}
				}
				for (int j = 0; j < 8; ++j)
				{
					depth++;
					nodes.at(idx + j).initialize(depth, nodes.at(idx + j).triangles);
				}
			}

		}

		bool rayTriangleIntersection(const Triangle & T, const vec3& s, const vec3& v, float& t, vec3 & normal, vec3& ip)
		{
			float denum = dot(T.N, v);
			if (denum == 0)
			{
				//parallel
				return false;
			}

			float t1 = -1 * (T.D + dot(T.N, s)) / denum;
			if (t1 < 0)
			{
				//no intersection
				return false;
			}
			vec3 ips = s + (t1*v);
			float area = 0;
			//abp, apc, pcb
			for (int i = 0; i < 3; i++)
			{
				vec3 p = T.p[i];
				vec3 q = cross(T.e[i], (ips - p));
				area += q.magnitude();
			}

			float temporary = area * T.oneOverTwiceArea;
			if (temporary <= 1.001)
			{
				//we have an intersection
				if (t1 < t)
				{
					normal = T.N;
					ip = ips;
					t = t1;
					return true;
				}
			}
		}
		
		bool traverseTree(const vec3& s, const vec3& v, vec3& normal, vec3& ip, vec3& color, float& t)
		{
			OctreeNode* node;
			std::stack<OctreeNode*> stk;
			stk.push(&(nodes.at(0)));
			//since the root will always be the first item in the nodes vector
			while (!stk.empty())
			{
				node = stk.top();
				stk.pop();
				float initT = t;

				// check for intersection!

				if (rayBoxIntersection(node->planes, s, v))
				{
					if (node->children.size() == 0)
					{
						//a leaf
						float t1 = t;
						vec3 n = vec3(0, 0, 0);
						vec3 i = vec3(0, 0, 0);
						for (Triangle& T : node->triangles)
						{
							rayTriangleIntersection(T, s, v, t, normal, ip);
						}
						if (t != initT)
						{
							color = node->color;
							return true;
						}
					}
					else
					{
						//means we aint at a leaf just yet!
						for (int i = 0; i < 8; i++)
						{
							int temp = node->children.at(i);
							if (temp < 0)
								continue;
							//temp will only be < 0 if it was a leaf
							stk.push(&(nodes.at(temp)));
						}
					}
				}

			}
			return false;
		}

};

