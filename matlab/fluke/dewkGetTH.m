function output = dewkGetTH(s)
    url = strcat(s.ControllerURL, '/read');
    output = webread(url);
end
