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
    url = strcat(s.CameraURL, '/feature/', featurename);
    tmp = webread(url);
    val = tmp.value;
end
