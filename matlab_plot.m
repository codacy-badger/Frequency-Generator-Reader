fileID = fopen('Output/voltage output.txt','r');
formatSpec = '%f';
A = fscanf(fileID,formatSpec);
fclose(fileID);
plot(A);