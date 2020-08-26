function dacOutput(s, channel, voltage)
    url = strcat(s.DACURL, '/output');
    s2 = struct();
    s2.channel = channel;
    s2.voltage = voltage;
    opts = weboptions("MediaType", "application/json");
    webwrite(url, s2, opts);
end
