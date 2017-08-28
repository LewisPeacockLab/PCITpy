%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [] = plot_boot_results(analysis_id, write_dir, x, y_all_runs, weight_all_runs, alpha, resolution, credible_interval, image_format, n_bins, varargin)

root_dir = pwd;
total_bootstrap_runs = varargin{2};

sample_idx(1) = floor(total_bootstrap_runs * (alpha / 2));
if sample_idx(1) == 0, sample_idx(1) = ceil(total_bootstrap_runs * (alpha / 2)); end
sample_idx(2) = ceil(total_bootstrap_runs * (alpha / 2));
sample_idx(3) = floor(total_bootstrap_runs * (1 - (alpha / 2)));
if sample_idx(3) == 0, ceil(total_bootstrap_runs * (1 - (alpha / 2))); end
sample_idx(4) = ceil(total_bootstrap_runs * (1 - (alpha / 2)));

sorted_y_all_runs = sort(y_all_runs);
envelope_bounds = NaN(2, length(x));
envelope_bounds(1, :) = (sorted_y_all_runs(sample_idx(1), :) + sorted_y_all_runs(sample_idx(2), :)) / 2;
envelope_bounds(2, :) = (sorted_y_all_runs(sample_idx(3), :) + sorted_y_all_runs(sample_idx(4), :)) / 2;

legend_str = '';
if length(varargin) == 3
	results_dir = fullfile(root_dir, 'results');
	read_dir = fullfile(results_dir, varargin{3});
	% Load the original .mat file
	importance_sampler_mat = load(sprintf('%s/%s_importance_sampler.mat', read_dir, varargin{3}));
	% Find the particles / curves indices that are theory consistent
	th_con_idx = family_of_curves(importance_sampler_mat.analysis_settings.curve_type, 'count_particles', importance_sampler_mat.curve_params);
	% Using the above indices fetch the sum of the particle weights. This is what we call / refer throughout as p(theory consistent)
	% Here I am fetch the weights from the last em eiteration hence the 'end'
	weight_original = sum(importance_sampler_mat.normalized_weights(end, th_con_idx));

	% Get the weighted sum of the curves over all particles and the associated credible interval. This is the blue line and the grey envelope around the blue line
	weighted_curve_struct = common_to_all_curves(importance_sampler_mat.analysis_settings.curve_type, 'weighted_curve', importance_sampler_mat, credible_interval, resolution);
	y_original = weighted_curve_struct.y_final;
	legend_str = 'Original recovered curve';
else
	weight_original = mean(weight_all_runs);
	y_original = mean(y_all_runs);
	legend_str = 'Mean(bootstrap runs)';
end
proportion = sum(weight_all_runs > 0.5) / length(weight_all_runs);
proportion_str = sprintf('proportion(runs)>0.5=%0.2f', proportion);

% Plot the curve
figure(); set(gcf, 'Position', [50, 900, 1200, 500]);

subplot(1, 2, 1);
color = [107, 107, 107] ./ 255; transparency = 0.4;
hhh = jbfill(x, envelope_bounds(1, :), envelope_bounds(2, :), color, color, 0, transparency); hold on;
% hAnnotation = get(hhh, 'Annotation');
% hLegendEntry = get(hAnnotation', 'LegendInformation');
% set(hLegendEntry, 'IconDisplayStyle', 'off');
h2 = plot(x, y_original, 'b-', 'LineWidth', 2);

ylabel('Change in Memory Strength', 'FontSize', 12, 'FontName', 'Helvetica');
ylim([-1, 1]);
xlabel('Activation', 'FontSize', 12, 'FontName', 'Helvetica');
xlim([0, 1]);

grid on; set(gca, 'Layer', 'top');
title(sprintf('%d bootstrap runs, recovered curves', total_bootstrap_runs));
legend([h2(1), hhh(1)], legend_str, sprintf('%%95 confidence interval'), 'Orientation', 'Horizontal');

sorted_weights = sort(weight_all_runs);
wgt_lb = (sorted_weights(sample_idx(1)) + sorted_weights(sample_idx(2))) / 2;
wgt_ub = (sorted_weights(sample_idx(3)) + sorted_weights(sample_idx(4))) / 2;

subplot(1, 2, 2);
numbers = hist(weight_all_runs, n_bins);
hist(weight_all_runs, n_bins); hold on;
h = findobj(gca, 'Type', 'patch'); set(h, 'FaceColor', [255,193,193] ./ 255, 'EdgeColor', 'w');
hAnnotation = get(h, 'Annotation');
hLegendEntry = get(hAnnotation', 'LegendInformation');
set(hLegendEntry, 'IconDisplayStyle', 'off');

h1 = plot(weight_original, 0:3, 'b*');
h2 = plot([repmat(wgt_lb, 1, 4), repmat(wgt_ub, 1, 4)], [0:3, 0:3], 'b*', 'Color', color, 'Marker', '*');

ylabel('Count', 'FontSize', 12, 'FontName', 'Helvetica');
ylim([0, max(numbers)+5]);
xlabel('Distribution of posterior weights', 'FontSize', 12, 'FontName', 'Helvetica');
xlim([-0.02, 1.02]);
title(sprintf('%d bootstrap runs, posterior weights\n%s', total_bootstrap_runs, proportion_str));
legend([h1(1), h2(1)], legend_str, sprintf('%%95 confidence interval'), 'Location', 'NorthWest', 'Orientation', 'Vertical');

file_name = sprintf('%s/%s_bootstrap_results', write_dir, analysis_id);
savesamesize(gcf, 'file', file_name, 'format', image_format);
disp(sprintf('Bootstrap results plot is saved as %s.%s', file_name, image_format));
