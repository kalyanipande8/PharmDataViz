/* Authored-but-not-executed reference: the real SAS ODS Graphics
   workflow this visualization suite would use to generate
   submission-ready figures in production. No SAS installation is
   available in this environment, so src/visualization_suite.py
   implements the identical reusable per-endpoint plotting logic in
   Python/matplotlib as the executed mirror, and all measured
   results in this repo come from that mirror. */

%macro plot_endpoint(measure=, outpath=);
    ods graphics / imagename="&measure" imagefmt=png;
    ods listing gpath="&outpath";
    proc sgplot data=endpoints;
        series x=VISIT y=&measure / group=ARM markers;
        xaxis label="Visit";
        yaxis label="&measure";
    run;
    ods listing close;
%mend plot_endpoint;

%macro generate_all_figures(measures=, outpath=);
    %local i measure;
    %do i = 1 %to %sysfunc(countw(&measures));
        %let measure = %scan(&measures, &i);
        %plot_endpoint(measure=&measure, outpath=&outpath);
    %end;
%mend generate_all_figures;

%generate_all_figures(
    measures=symptom_score function_score qol_score pain_score mobility_score
             fatigue_score alt_level ast_level creatinine heart_rate systolic_bp wbc_count,
    outpath=/output/figures
);
