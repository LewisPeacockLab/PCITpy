%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [] = plot_scram_results(analysis_id, write_dir, weight_all_runs, resolution, image_format, n_bins, varargin)

root_dir = pwd;
total_scramble_runs = varargin{2};

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
	legend_str = 'Original recovered curve';
else
	weight_original = mean(weight_all_runs);
	legend_str = 'Mean(scramble runs)';
end
pval = sum(weight_all_runs >= weight_original) / (total_scramble_runs + 1);

% Plot the curve
figure(); set(gcf, 'Position', [50, 900, 600, 600]);

numbers = hist(weight_all_runs, n_bins);
hist(weight_all_runs, n_bins); hold on;
h = findobj(gca, 'Type', 'patch'); set(h, 'FaceColor', [255,193,193] ./ 255, 'EdgeColor', 'w');
hAnnotation = get(h, 'Annotation');
hLegendEntry = get(hAnnotation', 'LegendInformation');
set(hLegendEntry, 'IconDisplayStyle', 'off');

plot(weight_original, 0:3, 'b*');

ylabel('Count', 'FontSize', 15, 'FontName', 'Helvetica');
ylim([0, max(numbers)+5]);
xlabel('Distribution of posterior weights', 'FontSize', 15, 'FontName', 'Helvetica');
xlim([-0.02, 1.02]);
title(sprintf('%d scramble samples posterior weights\npval=%0.4f', total_scramble_runs, pval));
legend(legend_str, 'Orientation', 'Horizontal');

file_name = sprintf('%s/%s_scramble_results', write_dir, analysis_id);
savesamesize(gcf, 'file', file_name, 'format', image_format);
disp(sprintf('Scramble results plot is saved as %s.%s', file_name, image_format));