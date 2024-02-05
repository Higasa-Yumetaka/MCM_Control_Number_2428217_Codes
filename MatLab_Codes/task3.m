clc
clear all
%%
% Determine the number of search and rescue vessels and draw a trajectory map
number=1;%number<R/(2*r)
t_sum=zeros(1,number);
n_min=0;
for n=1:1:number
        % search radius
        R=200;
        % Sonar scan radius
        r=10;
        % Parameters that define the spiral
        a = 2*r*n; % Coil spacing parameters of the spiral
        b = 3; % spiral radius growth rate
        % Define the extent of the spiral
        theta = linspace(0, (R-a)/b, 500); % Radius 200, 100000 points
        distance=a + b*theta;
        figure;
        for i=1:1:n
            x = distance .* cos(theta+2*i*pi/n)+ location_1(1);
            y = distance .* sin(theta+2*i*pi/n)+ location_1(2);
            plot([0, a .* cos(2*i*pi/n)], [0, a .* sin(2*i*pi/n)], 'o-');hold on
            plot(x, y);hold on;
        end
        % Define arc length integral expression
        dr_dtheta=b;%Spiral derivative
        arc_length_expression = @(theta) sqrt((a + b*theta).^2 + dr_dtheta.^2);%路程与时间t
        %The relationship between success rate and time t
        % Calculate arc length
        arc_length = integral(arc_length_expression, 0, (R-a)/b);
        % Calculate scan time
        depth=linspace(3000, 50000, (arc_length/(2*a)+1));%depth!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        t_per=depth./750.+300;%The speed of sound propagates at every point
        v=6;
        t_sum(n)=arc_length/v+sum(t_per(:));%Calculate total time
end
%Number of ships versus time graph
% figure;
% N=1:number;
% plot(N,t_sum)
%Arc length versus time
% %%
% %The relationship between search and rescue success rate and time
% % Parameter settings
% k = 1;
% t0 = 6;
% 
% % Time from 0 to 12 hours
% t_continuous = 0:0.1:12;
% 
% % sigmoid function
% p_continuous = 1 ./ (1 + exp(k * (t_continuous - t0)));
% 
% % Take 10 time points for discretization
% num_discrete_points = 10;
% t_discrete = linspace(0, 12, num_discrete_points);
% p_discrete = interp1(t_continuous, p_continuous, t_discrete, 'pchip');
% 
% % Plot original curves and discrete points
% figure;
% plot(t_continuous, p_continuous, 'LineWidth', 2, 'DisplayName', 'original curve');
% hold on;
% scatter(t_discrete, p_discrete, 100, 'r', 'filled', 'DisplayName', 'discrete point');
% title('The relationship between search and rescue success rate and time');
% xlabel('Time (hours)');
% ylabel('Success rate');
% legend('show');
% grid on;
% 
% %%
% % ARIMA model preprocessing
% % Since the ARIMA model needs to process non-seasonal data, we assume that the necessary difference processing has been performed on the data, and the original discrete data is used directly here.
% 
% % Select ARIMA model order
% p = 2;  % autoregressive order
% d = 2;  % Differential order
% q = 2;  % moving average order
% 
% % Modeling, use p_discrete directly, but need to convert it to column vector
% model = arima(p, d, q);
% fit = estimate(model, p_discrete(:));
% 
% % Model diagnosis (use infer to get residuals)
% figure;
% residuals = infer(fit, p_discrete(:));
% subplot(2, 1, 1);
% plot(t_discrete(:), residuals, 'LineWidth', 2);
% title('residual');
% xlabel('Time (hours)');
% ylabel('residual');
% grid on;
% 
% subplot(2, 1, 2);
% autocorr(residuals);
% title('ACF of residuals');
% grid on;
% 
% % predict
% num_forecast_steps = 1;  % Set the number of time steps for prediction
% [forecast, forecastMSE] = forecast(fit, num_forecast_steps, 'Y0', p_discrete(:));
% 
% % Draw prediction curve
% figure;
% plot(t_discrete, p_discrete, 'LineWidth', 2, 'DisplayName', 'The actual data');
% hold on;
% plot([t_discrete(end), t_discrete(end) + 1:num_forecast_steps], forecast', 'r--', 'LineWidth', 2, 'DisplayName', 'Predicted data');
% title('ARIMA model forecast');
% xlabel('Time (hours)');
% ylabel('Success rate');
% legend('show');
% grid on;
% 
% %%
% % Boxplot plotting using residuals and predicted values
% % In order to display two different bins explicitly, we need to have two sets of data---residuals (diff_data) and predicted values (forecast_data)
% % Residuals is used here as diff_data
% 
% % Make sure all data are column vectors
% diff_data = residuals; % The residual data is already a column vector
% forecast_data = forecast; % The residual data is already a column vector
% 
% % Create a large data array and a corresponding grouped array
% boxplotData = [diff_data; forecast_data]; % Merge data
% groups = [repmat({'Diff'}, length(diff_data), 1); repmat({'Forecast'}, length(forecast_data), 1)]; % Date goes
% 
% % Draw a boxplot
% figure;
% boxplot(boxplotData, groups);
% title('Box plot of residuals versus predicted data');
% ylabel('numerical value');
%%
% % time series cross validation
% num_folds =6;  % time series cross validation
% fold_size = floor(num_discrete_points / num_folds);  % 计算每折的大小
% rmse_values = zeros(1, num_folds);  % Used to store the RMSE of each fold
% 
% figure;
% 
% for fold = 1:num_folds
%     % Divide training set and test set
%     test_indices = (fold - 1) * fold_size + 1 : fold * fold_size;
%     train_indices = setdiff(1:num_discrete_points, test_indices)';
%     
%     % Divide training set and test set
%     train_data = p_discrete(train_indices);
%     test_data = p_discrete(test_indices);
%     
%     % Train an ARIMA model
%     model = arima('ARLags',1,'D',1,'MALags',1);
%     fit = estimate(model, train_data);
%     
%     % Train an ARIMA model
%     num_test_steps = length(test_indices);
%     forecast = forecast(fit, num_test_steps);
%     
%     % Calculate prediction error
%     rmse = sqrt(mean((forecast - test_data).^2));
%     
%     % Store RMSE value
%     rmse_values(fold) = rmse;
%     
%     % Plot actual and forecast data
%     subplot(num_folds, 1, fold);
%     plot(t_discrete, p_discrete, 'LineWidth', 2, 'DisplayName', 'The actual data');
%     hold on;
%     plot(t_discrete(train_indices), train_data, 'b-', 'LineWidth', 2, 'DisplayName', 'training data');
%     plot(t_discrete(test_indices), forecast, 'r--', 'LineWidth', 2, 'DisplayName', 'Forecast data');
%     scatter(t_discrete(test_indices), test_data, 100, 'g', 'filled', 'DisplayName', 'Test Data');
%     title(['number of folds ', num2str(fold)]);
%     xlabel('Time (hours)');
%     ylabel('Success rate');
%     legend('show');
%     grid on;
%     
%     % Display fold and corresponding RMSE
%     text(t_discrete(test_indices(1)), max(p_discrete), ['RMSE = ' num2str(rmse)], 'VerticalAlignment', 'top', 'FontSize', 8);
% end
% 
% % Calculate mean RMSE and error bars
% avg_rmse = mean(rmse_values);
% std_rmse = std(rmse_values);
% 
% fprintf('\nAverage RMSE = %.4f\n', avg_rmse);
% fprintf('RMSE error bars = %.4f\n', std_rmse);
% 
% % Show mean RMSE and error bars
% figure;
% bar(avg_rmse);
% hold on;
% errorbar(1, avg_rmse, std_rmse, 'r', 'LineWidth', 2);
% title('Mean RMSE and error bars');
% xlabel('number of folds');
% ylabel('RMSE');
% grid on;