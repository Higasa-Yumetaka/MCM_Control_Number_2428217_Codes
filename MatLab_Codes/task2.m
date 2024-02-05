clc
clear
% Initialize device data
devices = {'multibeam sonar', 'side scan sonar', 'AUV','ROV', 'Drones for surface searches', 'Underwater search signal repeater','Deep sea salvage system'};
costs = [40000, 40000, 10000,10000,180000,20000,10000]; % Total cost of each piece of equipment (purchase, maintenance, operation)
ranges = [300, 500, 50,5,200000,1000,2000]; % Search and rescue scope
accuracies = [2000, 50, 800,1000,10,200,2000]; % Accuracy
reliabilities = [100, 6, 70,120,20,50,600]; % Reliability
%Normalized
costs_new=(costs-min(costs))./(max(costs)-min(costs))+1;
ranges_new=(ranges-min(ranges))./(max(ranges)-min(ranges));
accuracies_new=(accuracies-min(accuracies))./(max(accuracies)-min(accuracies));
reliabilities_new=(reliabilities-min(reliabilities))./(max(reliabilities)-min(reliabilities));
% Weight setting, the weight comes from the analytic hierarchy process
w_range=0.5954;%0.3866
w_accuracy=0.2764;%0.2402
w_reliability=0.1283;%0.3732
% cost benefit ratio calculation
CERs = zeros(size(devices));
for i = 1:length(devices)
    E = w_range * ranges_new(i) + w_accuracy * accuracies_new(i) + w_reliability * reliabilities_new(i);
    C = costs_new(i);
    CERs(i) = E / C;
end

% Êä³ö½á¹û
for i = 1:length(devices)
    fprintf('%s ¡¯s cost-benefit ratio is %f\n', devices{i}, CERs(i));
end
[~, bestDeviceIndex] = max(CERs);
fprintf('The recommended equipment is %s\n', devices{bestDeviceIndex});
