#include "../include/PrimitivesFamily.hpp"

#include <vector>
#include <list>

#ifndef ATTRIBUTE_OPENING_PRIMITIVES_FAMILY_H
#define ATTRIBUTE_OPENING_PRIMITIVES_FAMILY_H

class AttributeOpeningPrimitivesFamily: public PrimitivesFamily{
  
  protected:
    float* attrs_increasing;
    float maxCriterion;
    std::list<float> thresholds;
    std::list<NodeCT*> nodesWithMaximumCriterium;
    
    void initializeRestOfImage(float threshold);
    void initializeNodesWithMaximumCriterium();
    
  public:
    AttributeOpeningPrimitivesFamily(ComponentTree* tree,  float* attr, float maxCriterion);

    AttributeOpeningPrimitivesFamily(ComponentTree* tree,  float* attrs_increasing, float maxCriterion, int deltaMSER);
    
    ~AttributeOpeningPrimitivesFamily();

    bool isSelectedForPruning(NodeCT* node) override; //first Node in Nr(i)

    virtual bool hasNodeSelectedInPrimitive(NodeCT* node) override; //has node selected inside Nr(i)

    virtual std::list<NodeCT*> getNodesWithMaximumCriterium() override; 

    virtual ComponentTree* getTree() override;

    virtual int* getRestOfImage() override;

    virtual int getNumPrimitives() override;

    std::list<float> getThresholdsPrimitive();

    

};

#endif





