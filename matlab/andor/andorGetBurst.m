function ary = andorGetBurst(s, frames, fps)

    writeopts = weboptions('Timeout', Inf, 'MediaType', 'application/json');
    opts = weboptions('Timeout', Inf);

    s2 = struct();
    s2.fps = fps;
    s2.frames = frames;

    webwrite(strcat(s.CameraURL, '/burst/setup'), s2, writeopts);
    ary = [];

    for i = 1:frames
        websave('dummy.fits', strcat(s.CameraURL, '/burst/frame'), 'fmt', 'fits', opts);
        ary(:,:,i) = fitsread('dummy.fits');
    end
    
end