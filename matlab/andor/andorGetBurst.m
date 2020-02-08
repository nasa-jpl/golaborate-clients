function ary = andorGetBurst(s, frames, fps)
% img_array = andorGetBurst(camera struct, number of frames, frames per second).
% Take a burst of images from an Andor camera.  The images are saved into an array
% arranged so that the 3rd dimension walks through the images.

    writeopts = weboptions('Timeout', Inf, 'MediaType', 'application/json');
    opts = weboptions('Timeout', Inf);

    s2 = struct();
    s2.fps = fps;
    s2.frames = frames;

    webwrite(strcat(s.CameraURL, '/burst/setup'), s2, writeopts);
    AOI = andorGetAOI(s);
    ary = zeros(AOI.height, AOI.width, frames);

    for i = 1:frames
        websave('dummy.fits', strcat(s.CameraURL, '/burst/frame'), 'fmt', 'fits', opts);
        ary(:,:,i) = fitsread('dummy.fits');
    end
    
end
