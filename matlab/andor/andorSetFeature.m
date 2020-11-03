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
    options = weboptions('MediaType', 'application/json');
    url = strcat(s.CameraURL, '/feature/', featurename);
    s_tmp = struct();
    s_tmp.value = value;
    ret = webwrite(url, s_tmp, options);

end
