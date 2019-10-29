function s = nktMainModuleStatus(NKTs)
     path = strcat(NKTs.NKTSuperKRoot, "/main-module-status");
     s = webread(path);
end