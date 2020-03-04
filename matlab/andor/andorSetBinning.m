function andorSetBinning(s, fctr)
%andorSetBinning(s, tSec)
%   Sets the binning to (fctr x fctr) pixels

    s2 = struct();
    s2.h = fctr;
    s2.v = fctr;
    options = weboptions('MediaType', 'application/json');
    url = [s.CameraURL,'/binning'];
    webwrite(url, s2, options)
end
