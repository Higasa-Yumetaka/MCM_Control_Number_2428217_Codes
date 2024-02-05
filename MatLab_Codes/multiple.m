clc
clear
%%
% Three known coordinate points
location_1=[0,0];
location_2=[-400,600];
location_3=[800,400];
% Calculate the coordinates of the fourth point
location_start=[(location_1(1)+location_2(1)+location_3(1))/3,(location_1(2)+location_2(2)+location_3(2))/3];

% Store the x-coordinates and y-coordinates of all points in two arrays
x = [location_1(1), location_2(1), location_3(1), location_start(1)];
y = [location_1(2), location_2(2), location_3(2), location_start(2)];

% draw points
figure; % Create a graphics window
plot(x, y, 'o'); % 'o'Specifies to draw points instead of lines
grid on; % show grid

% Set axis labels
xlabel('X Coordinate');
ylabel('Y Coordinate');
title('Display of Points with Connections');

% Draw lines from location_start to three other points
hold on; % hold on; % Draw lines from location_start to three other points
plot([location_start(1), location_1(1)], [location_start(2), location_1(2)], 'k-');
plot([location_start(1), location_2(1)], [location_start(2), location_2(2)], 'k-');
plot([location_start(1), location_3(1)], [location_start(2), location_3(2)], 'k-');

% Add text labels to each point
text(location_1(1), location_1(2), 'Location 1', 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
text(location_2(1), location_2(2), 'Location 2', 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
text(location_3(1), location_3(2), 'Location 3', 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
text(location_start(1), location_start(2), 'Location Start', 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');

% Adjust axis ranges to better display points and lines
axis([min(x)-100 max(x)+100 min(y)-100 max(y)+100]);
%%
% location_1
% Determine the number of search and rescue vessels and draw a trajectory map
number=2;%number<R/(2*r)
t_sum=zeros(1,number);
n_min=0;
for n=1:1:number
        % search radius
        R=200;
        % Determine sonar radius
        r=10;
        % Parameters that define the spiral
        a = 2*r*n; % Coil spacing parameters of the spiral
        b = 3; % spiral radius growth rate
        % Define the extent of the spiral
        theta = linspace(0, (R-a)/b, 500);
        distance=a + b*theta;
        for i=1:1:n
            x = distance .* cos(theta+2*i*pi/n)+ location_1(1);
            y = distance .* sin(theta+2*i*pi/n)+ location_1(2);
            plot([location_1(1), location_1(1)+a .* cos(2*i*pi/n)], [location_1(2), location_1(2)+a .* sin(2*i*pi/n)], 'o-');hold on
            plot(x, y);hold on;
        end
        % Define arc length integral expression
        dr_dtheta=b;%Spiral derivative
        arc_length_expression = @(theta) sqrt((a + b*theta).^2 + dr_dtheta.^2);%路程与时间t
        %The relationship between success rate and time t
        % Calculate arc length
        arc_length = integral(arc_length_expression, 0, (R-a)/b);
        %Calculate scan time
        depth=linspace(3000, 50000, (arc_length/(2*a)+1));%depth
        t_per=depth./750.+300;%The speed of sound propagates at every point
        v=6;
        t_sum(n)=arc_length/v+sum(t_per(:));%Calculate total time
end
%%
% location_2
% Determine the number of search and rescue vessels and draw a trajectory map
number=2;%number<R/(2*r)
t_sum=zeros(1,number);
n_min=0;
for n=1:1:number
        % search radius
        R=200;
        % Determine sonar radius
        r=10;
        % Parameters that define the spiral
        a = 2*r*n; % Coil spacing parameters of the spiral
        b = 3; % spiral radius growth rate
        % Define the extent of the spiral
        theta = linspace(0, (R-a)/b, 500);
        distance=a + b*theta;
        for i=1:1:n
            x = distance .* cos(theta+2*i*pi/n)+ location_2(1);
            y = distance .* sin(theta+2*i*pi/n)+ location_2(2);
            plot([location_2(1), location_2(1)+a .* cos(2*i*pi/n)], [location_2(2), location_2(2)+a .* sin(2*i*pi/n)], 'o-');hold on
            plot(x, y);hold on;
        end
        dr_dtheta=b;
        arc_length_expression = @(theta) sqrt((a + b*theta).^2 + dr_dtheta.^2);
        arc_length = integral(arc_length_expression, 0, (R-a)/b);
        depth=linspace(3000, 50000, (arc_length/(2*a)+1));
        t_per=depth./750.+300;
        v=6;
        t_sum(n)=arc_length/v+sum(t_per(:));
end
%%
%location_3
number=2;%number<R/(2*r)
t_sum=zeros(1,number);
n_min=0;
for n=1:1:number
        R=200;
        r=10;
        a = 2*r*n;
        b = 3;
        theta = linspace(0, (R-a)/b, 500);
        distance=a + b*theta;
        for i=1:1:n
            x = distance .* cos(theta+2*i*pi/n)+ location_3(1);
            y = distance .* sin(theta+2*i*pi/n)+ location_3(2);
            plot([location_3(1), location_3(1)+a .* cos(2*i*pi/n)], [location_3(2), location_3(2)+a .* sin(2*i*pi/n)], 'o-');hold on
            plot(x, y);hold on;
        end
        dr_dtheta=b;
        arc_length_expression = @(theta) sqrt((a + b*theta).^2 + dr_dtheta.^2);
        arc_length = integral(arc_length_expression, 0, (R-a)/b);
        depth=linspace(3000, 50000, (arc_length/(2*a)+1));
        t_per=depth./750.+300;
        v=6;
        t_sum(n)=arc_length/v+sum(t_per(:));
end