function val = andorGetFeature(s,featurename)
%ret = andorGetFeature(s,featurename)
%   Gets the current value for a feature of the Andor Neo SDK
%   
%   Inputs:
%       s - Structure containing CameraURL 
%       featurename - String - name of the Andor SDK feature
%   Outputs:
%       val - feature value 
%

    % Get feature type from SDK
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
    
    url = strcat(s.CameraURL, '/feature/', featurename);
    tmp = webread(url);
    val = eval(['tmp.',featurekey]);
    
end
