function andorSetAOI(s)
%andorSetAOI(s)
%   Sets the AOI features on the Andor Neo. 
%   
%   Inputs:
%       s - Structure containing: 
%           CameraURL - URL of Neo camera (including port num) 
%           nbin - int - Binning number 
%           usesubwindow - bool - if true, use subwindow. otherwise, use
%                                   full (binned) frame.
%           subwindowsize - int - size of the subwindow. must be even. 
%           centerrow - int - row index of center pixel 
%           centercol - int - col index of center pixel 
%

    %%- Define the Andor ADK features for the desired AOI

    % convert nbin (an integer) into a string like '1x1','2x2',...
    bin_str = [num2str(s.nbin),'x',num2str(s.nbin)];
    s.AOIBinning = bin_str;
    
    % define AOIWidth, AOILeft, AOIHeight, AOITop
    if(s.usesubwindow)
        N = s.subwindowsize;
        cr = s.centerrow;
        cc = s.centercol;

        s.AOIWidth = N;
        s.AOIHeight = N;
        s.AOILeft = cc - N/2 - 1;
        s.AOITop = cr - N/2 - 1;
    else
        s.AOIWidth = 2560;
        s.AOIHeight = 2160;
        s.AOILeft = 1;
        s.AOITop = 1;
    end


    %%- Set the AOI features (in order recommended by SDK manual)
    
    andorSetFeature(s,'AOIBinning',s.AOIBinning);
    andorSetFeature(s,'AOIWidth',s.AOIWidth);
    andorSetFeature(s,'AOILeft',s.AOILeft);
    andorSetFeature(s,'AOIHeight',s.AOIHeight);
    andorSetFeature(s,'AOITop',s.AOITop);
    
end
