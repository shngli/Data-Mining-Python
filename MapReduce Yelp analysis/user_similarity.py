# Author: Sheng Li
# Write the functions to calculate the Jaccard similarity between users and output users >= 0.5 similarity
# with a user defined as a set of businesses reviewed {BizA, BizB, BizC}

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from itertools import combinations

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    
    # First map: go through every record and return tuples of user_id & every business_id that the user reviewed.    
    def user_biz(self, _, record):
        if record['type'] == 'review':
            yield record['user_id'], record['business_id']
    
    # First reduce: take each user and create a set of business_ids for each place that they reviewed. 
    # Output will be  user_id, [business_id1, business_id2, business_id3]
    def user_biz_set(self, user_id, business_ids):
        yield user_id, list(business_ids)
    
    # Second map: 
    def jaccard_combi(self, user_id, user_biz_ids):  
        yield 'foo', [user_id, user_biz_ids]
    
    # Second reduce: calculate the jaccard similarity between two users based on the business_id of their reviews
    # and aggregate the pair of users where their coefficient is greater than or equal to 0.5
    def jaccard_similarity(self, _, users):
        for user1, user2 in combinations(users, 2):
            
            biz_total = (set(user1[1] + user2[1]))
            union = len(biz_total)           
            
            biz_common = (set(user1[1]) & set(user2[1]))            
            intersection = len(biz_common)
            
            jaccard_coefficient = float(intersection) / float(union)
            '''
            #Sample output
            print "---------"
            print "user 1: " + user1[0] + " : " + str(user1[1])
            #user 1: LjQkuDdza3D7hD8-iAOrrg : ['FV16IeXJp2W6pnghTz2FAw', 'Yq8LiVymGA7vBpGCQuDfRw', 'nzQJqTrcazg23EjdaHgqDg']
            print "user 2: " + user2[0] + " : " + str(user2[1])
            #user 2: NoZQnBtkjE1Syx12SY5a3g : ['FV16IeXJp2W6pnghTz2FAw', 'Yq8LiVymGA7vBpGCQuDfRw']
            print
            print "biz_total: %s" % biz_total 
            #biz_total: set(['Yq8LiVymGA7vBpGCQuDfRw', 'nzQJqTrcazg23EjdaHgqDg', 'FV16IeXJp2W6pnghTz2FAw'])
            print "biz_common: %s" % biz_common
            #biz_common: set(['Yq8LiVymGA7vBpGCQuDfRw', 'FV16IeXJp2W6pnghTz2FAw'])
            print
            print "jaccard intersection: %s" % intersection
            #jaccard intersection: 2
            print "jaccard union: %s" % union
            #jaccard union: 3
            print "jaccard coefficient: %s" % jaccard_coefficient
            #jaccard coefficient: 0.666666666667
            print   
            ''' 
            if jaccard_coefficient >= 0.5:
                yield [user1[0], user2[0]], jaccard_coefficient
    
    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <user_id, business_id>
        reducer1: <user_id, [business_ids]> (turn business_ids into a set)
        mapper2: <string, [user_id, [business_ids]]>
        reducer2: <[user1, user2], jaccard coefficient>
        """
        return [self.mr(mapper=self.user_biz, reducer=self.user_biz_set),
                self.mr(mapper=self.jaccard_combi, reducer=self.jaccard_similarity)]
        
        # Sample output
        #["---_j-GW5aCBtf62ihHwCw", "9jUs-okApB-BYUspnetcrw"]	1.0
        #["KtPxAUEcFLiG8Jl2IaP_HA", "NoZQnBtkjE1Syx12SY5a3g"]	0.5
        #["LjQkuDdza3D7hD8-iAOrrg", "NoZQnBtkjE1Syx12SY5a3g"]	0.6666666666666666


if __name__ == '__main__':
    UserSimilarity.run()
