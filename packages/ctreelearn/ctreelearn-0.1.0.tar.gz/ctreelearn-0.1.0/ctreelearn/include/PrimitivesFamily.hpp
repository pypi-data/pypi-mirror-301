#include "../include/NodeCT.hpp"
#include "../include/ComponentTree.hpp"
#include "../include/ComputerMSER.hpp"
#include "../include/AttributeComputedIncrementally.hpp"

#include <list>
#include <vector>


#ifndef PRIMITIVES_FAMILY_H
#define PRIMITIVES_FAMILY_H

class PrimitivesFamily{

  protected:
    
    ComponentTree* tree;

    std::vector<bool> selectedForFiltering; //mappping between index nodes and selected nodes

    int* restOfImage;

    int numPrimitives;

  public:

    virtual bool isSelectedForPruning(NodeCT* node) = 0; //first Node in Nr(i)

    virtual bool hasNodeSelectedInPrimitive(NodeCT* node) = 0; //has node selected inside Nr(i)

    virtual std::list<NodeCT*> getNodesWithMaximumCriterium() = 0; 

    virtual int* getRestOfImage() = 0;

    virtual int getNumPrimitives() = 0;

    virtual ComponentTree* getTree() = 0;
    
};

#endif



	

