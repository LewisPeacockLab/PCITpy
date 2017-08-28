function[p_wgts, y_final] = plot_figures(analysis_id, read_dir, write_dir, resolution, credible_interval, n_bins, image_format, visible_off)

% Load the target .mat file
importance_sampler_mat = load(sprintf('%s/%s_importance_sampler.mat', read_dir, analysis_id));

% Find the particles / curves indices that are theory consistent
th_con_idx = family_of_curves(importance_sampler_mat.analysis_settings.curve_type, 'count_particles', importance_sampler_mat.curve_params);

% Using the above indices fetch the sum of the particle weights. This is what we call / refer throughout as p(theory consistent)
% Here I am fetch the weights from the last em eiteration hence the 'end'
p_wgts = sum(importance_sampler_mat.normalized_weights(end, th_con_idx));


% Calculate the p-value that our beta1 is significantly different from 0
likelihood_ratio_test_for_beta1 = importance_sampler_mat.likratiotest;

% Calculate relative changes in fminunc over time
fminunc_fvals = importance_sampler_mat.exp_max_fval;
[max_fval, max_fval_iteration] = max(fminunc_fvals);
[min_fval, min_fval_iteration] = min(fminunc_fvals);
fminunc_val_change_dir = 'DEC';
fminunc_relative_value_name = 'max';
if max_fval_iteration > min_fval_iteration
	fminunc_val_change_dir = 'INC';
    fminunc_relative_value_name = 'min';
	fminunc_relative_change = ((max_fval - min_fval) / min_fval);
else
	fminunc_relative_change = ((max_fval - min_fval) / max_fval);
end



% Get the weighted sum of the curves over all particles and the associated credible interval. This is the blue line and the grey envelope around the blue line
weighted_curve_struct = common_to_all_curves(importance_sampler_mat.analysis_settings.curve_type, 'weighted_curve', importance_sampler_mat, credible_interval, resolution);
x_final = weighted_curve_struct.x_final;
y_final = weighted_curve_struct.y_final;
interval = weighted_curve_struct.interval;

% Plot the curve
if visible_off
	figure('visible', 'off');
else
	figure();
end
set(gcf, 'Position', [50, 900, 500, 500]);

color = [107, 107, 107] ./ 255; transparency = 0.4;
hhh = jbfill(x_final, interval(1, :), interval(2, :), color, color, 0, transparency); hold on;
plot(x_final, y_final, 'b-', 'LineWidth', 2);

ylabel('Change in Memory Strength', 'FontSize', 15, 'FontName', 'Helvetica');
ylim([-1, 1]);
xlabel('Activation', 'FontSize', 15, 'FontName', 'Helvetica');
xlim([0, 1]);

grid on; set(gca, 'Layer', 'top');
title(sprintf('P(theory consistent) = %0.4f', p_wgts));
file_name = sprintf('%s/%s_weighted_curve', write_dir, analysis_id);
print(gcf, sprintf('-d%s', image_format), '-painters', file_name);
disp(sprintf('1. Recovered curve plot is saved as %s.%s', file_name, image_format));

if visible_off
	figure('visible', 'off');
else
	figure();
end
set(gcf, 'Position', [50, 900, 1000, 1000]);

subplot(2, 2, 1);
beta_1 = importance_sampler_mat.hold_betas_per_iter(:, 2);
plot(0:importance_sampler_mat.analysis_settings.em_iterations, beta_1, 'bo-', 'MarkerFaceColor', 'b');

ylabel('beta 1');
ylim([-0.2, 2.2]);
xlabel('EM iterations');

title({'Beta 1 over em iterations' sprintf('P(Beta 1 = 0) = %0.6f',likelihood_ratio_test_for_beta1 )});
grid on; set(gca, 'Layer', 'top');

subplot(2, 2, 2);
hist(importance_sampler_mat.normalized_weights(end, :), n_bins); hold on;
h1 = plot(max(importance_sampler_mat.normalized_weights(end, :)), 1, 'ro', 'MarkerFaceColor', 'r');

ylabel('count', 'FontSize', 12, 'FontName', 'Helvetica');
xlabel('posterior weights' , 'FontSize', 12, 'FontName', 'Helvetica');

title({ sprintf('Distribution of posterior weights (%d iteration)', importance_sampler_mat.analysis_settings.em_iterations)  sprintf('sample max weight=%0.4f', max(importance_sampler_mat.normalized_weights(end, :))) });

grid on; set(gca, 'Layer', 'top');
legend([h1], 'Max weight');

subplot(2, 2, [3 4]);
fminunc_fvals = importance_sampler_mat.exp_max_fval;
plot(1:importance_sampler_mat.analysis_settings.em_iterations, fminunc_fvals, 'bo-', 'MarkerFaceColor', 'b');

ylabel('fminunc fval', 'FontSize', 12, 'FontName', 'Helvetica');
xlabel('EM iterations', 'FontSize', 12, 'FontName', 'Helvetica');

title({'fminunc fval over em iterations' sprintf('fminunc %s over iterations by %0.4f of %s fval',fminunc_val_change_dir,fminunc_relative_change,fminunc_relative_value_name)});
grid on; set(gca, 'Layer', 'top');

file_name = sprintf('%s/%s_report_plot', write_dir, analysis_id);
savesamesize(gcf, 'file', file_name, 'format', image_format);
disp(sprintf('2. Toolbox report plot is saved as %s.%s', file_name, image_format));
