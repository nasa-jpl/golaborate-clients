function dacOutputDN(s, channel, DN)
    url = strcat(s.DACURL, '/output-dn-16');
    s2 = struct();
    s2.channel = channel;
    s2.dn = DN;
    opts = weboptions("MediaType", "application/json");
    webwrite(url, s2, opts);
end
