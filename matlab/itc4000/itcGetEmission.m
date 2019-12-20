function on = itcGetEmission(s)
    url = strcat(s.ControllerURL, "/emission");
    s = webread(url);
    on = s.bool;
end