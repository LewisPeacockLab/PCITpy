for x = 1:1000
fname = fopen('imdif_importance_sampler_tacc2_template.txt','a');
fprintf(fname, 'batch_matlab.sh "imdif_bootstrap_run_importance_sampler_tacc2(1,%d)"\n',x)
fclose(fname)
end