function ret = andorSetFeature(s,featurename,value)
%ret = andorSetFeature(s,featurename,value)
%   Sets a feature on the Andor Neo to the desired value. 
%   
%   Inputs:
%       s - Structure containing CameraURL 
%       featurename - String - name of the Andor SDK feature
%       value - Value to set feature to (type should match type expected by the SDK)
%
%   Outputs:
%       ret - response from webwrite 
%

    listOfFeatureTypes = webread(strcat(s.CameraURL, '/feature'));
    featuretype = eval(['listOfFeatureTypes.',featurename]);

    %- Get featuretype key 
    if(strcmp(featuretype,'int'))
        featurekey = 'int';
    elseif(strcmp(featuretype,'bool'))
        featurekey = 'bool';
    elseif(strcmp(featuretype,'float'))
        featurekey = 'f64';
    else
        featurekey = 'str';
    end
    
    options = weboptions('MediaType', 'application/json');
    url = strcat(s.CameraURL, '/feature/', featurename);
    if(strcmp(featurekey,'str'))
        s_tmp.str = value;
    elseif(strcmp(featurekey,'bool'))
        s_tmp.bool = value;
    else
        eval(['s_tmp.',featurekey,'=',num2str(value),';']); 
    end
    ret = webwrite(url, s_tmp, options);
    
end
