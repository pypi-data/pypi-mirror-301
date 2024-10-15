#include <list>

#include "../include/NodeCT.hpp"
#include "../include/NodeRes.hpp"
#include "../include/PrimitivesFamily.hpp"

#ifndef RESIDUAL_TREE_H
#define RESIDUAL_TREE_H


class ResidualTree{

    protected:
      NodeRes* root;
      PrimitivesFamily* primitivesFamily;
      ComponentTree* tree;
      int* maxContrastLUT;
      int* associatedIndexesLUT;
      int numNodes;
      int* restOfImage;
      //std::list<NodeRes*> listNodes;
      NodeRes** nodes;

    public:
        ResidualTree(PrimitivesFamily* primitivesFamily);

        //void computerNodeRes(NodeCT *currentNode);

        void computerMaximumResidues();

        void createTree();

        int* reconstruction();

        ~ResidualTree();

        //std::list<NodeRes*> getListNodes();

        NodeRes* getRoot();

        NodeRes* getNodeRes(NodeCT* node);

        int* getMaxConstrastImage();

        int* filtering(float *attribute, float threshold, int* imgOutput);

        int* getAssociatedImage();

        int* getAssociatedColorImage();   

        int* getRestOfImage();

        ComponentTree* getCTree();

};


#endif