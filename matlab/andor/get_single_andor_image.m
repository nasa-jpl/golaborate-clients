clear; 

%% Camera URL

wfscam.CameraURL = 'http://192.168.100.184:8000';

%% Get features

sn = andorGetFeature(wfscam,'SerialNumber');
disp(['Serial number: ',sn]);

fwv=andorGetFeature(wfscam,'FirmwareVersion');
disp(['Firmware Version: ',fwv]);

ts = andorGetFeature(wfscam,'TemperatureStatus');
st = andorGetFeature(wfscam,'SensorTemperature');
disp(['Cooing status: ',ts,' ',num2str(st),'C'])

%% Set a feature 

andorSetFeature(wfscam,'FanSpeed','Off');

%% Set the exposure time 

andorSetExposureTime(wfscam,1e-3);
texp = andorGetExposureTime(wfscam);
disp(['Exposure time set to ',num2str(texp)]);

%%  Set subwindow  

wfscam.usesubwindow = false; 
wfscam.subwindowsize = 100;
wfscam.centerrow = 2160/2+1;
wfscam.centercol = 2560/2+1;
wfscam.nbin = 1;

andorSetAOI(wfscam)

%% Get the frame

im = andorGetFrame(wfscam, 'tmp.fits');

figure(1);imagesc(im); axis image; colorbar;  