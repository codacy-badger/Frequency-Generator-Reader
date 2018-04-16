fileID = fopen('Output/voltage output.txt','r');
formatSpec = '%f';
A = fscanf(fileID,formatSpec);
fclose(fileID);

configFileReader = fopen('Output/config.txt','r');
formatSpec = '%f';
C = fscanf(configFileReader,formatSpec);
fclose(configFileReader);

count = C(1,1);
scan_rate = C(2,1);
duration = count / scan_rate;

hertz = "Hz";

if (1000 < scan_rate) && (scan_rate < 1000000)
    scan_rate = scan_rate / 1000;
    hertz = "kHz";
elseif 1000000 <= scan_rate
    scan_rate = scan_rate / 1000000;
    hertz = "MHz";
end

str_format_scec = 'Received data scanned at %s %s for %d  seconds (%d elements)';
str = sprintf(str_format_scec, num2str(scan_rate), hertz, duration, count);

plot(A)
title(str)
xlabel([int2str(count) ' elements over ' int2str(duration) ' seconds'])
ylabel('Voltage')
savefig('Output/output_matlab_plot.fig')