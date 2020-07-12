from core.util import format_pii_object
from core import util

def combine_regex_and_context(regex_matches, context_matches, pii_type):
    final_matches = []
    
    for re_match in regex_matches:
        best_confidence = re_match.get('confidence')
        re_start = re_match.get('start')
        re_end = re_match.get('end')
        
        for con_match in context_matches:
            
            con_start = con_match.get('start')
            con_end = con_match.get('end')
            con_match_pct = con_match.get('match_pct')
            
            if re_start > con_end:
                distance = re_start - con_end
            else:
                distance = con_start - re_end
            
            distance = max(1, abs(distance) - 1)  # Distance should account for spacing and div by 0 errors
            
            confidence = 0.2 * (1.0 / (distance ** 0.1)) + 0.3 * con_match_pct + 0.5 * re_match.get('confidence')
            
            if confidence > best_confidence:
                best_confidence = confidence
        
        if(pii_type=='name' or pii_type=='company'):
            tagg=(util.preprocess_text(re_match['data']))
            str_data=re_match['data']
            flag=0     # For storing the tags location
            for i in range(0,len(tagg[0])):
                word=tagg[0][i][0]
                l_word=len(word)
                while(True):
                    if((str_data[flag:flag+l_word])==word):
                        if(tagg[0][i][1]=='NNP'):
                            if(best_confidence>0.4):
                                final_matches.append(format_pii_object(re_start+flag,re_start+flag+l_word,pii_type,best_confidence))
                        flag=flag+l_word
                        break
                    else:
                        flag=flag+1
        else:
            if(best_confidence>0.4):
                final_matches.append(format_pii_object(re_start, re_end, pii_type, best_confidence))
    
    return final_matches
