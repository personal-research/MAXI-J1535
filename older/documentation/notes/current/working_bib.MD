# Working Bibliography

## Reading List

### Priority: 
- [ ] SN20
- [ ] P21
- [ ] QPO2020

### Other: 
* [Evaluating the Impact of Missing Data Imputation
through the use of the Random Forest Algorithm](https://arxiv.org/ftp/arxiv/papers/0812/0812.2412.pdf#:~:text=Results%20indicate%20that%20Random%20Forests,when%20compared%20with%20autoassociative%20networks.)
* [Accuracy of random-forest-based imputation of missing data in the presence of non-normality, non-linearity, and interaction
](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-020-01080-1)
* [When do random forests fail?](https://proceedings.neurips.cc/paper/2018/file/204da255aea2cd4a75ace6018fad6b4d-Paper.pdf)
* [A survey on missing data in machine learning
](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-021-00516-9)
* [XGBoost: A Scalable Tree Boosting System](https://arxiv.org/pdf/1603.02754.pdf)
    * Section 3.4 discusses how XGBOOST natively deals with missing values
* [The Smallest Sample Size for the Desired Diagnosis Accuracy](https://www.iaras.org/iaras/filedownloads/ijoct/2017/028-0004(2017).pdf)
    * Cancer data...talks about XGBoost performance on small datasets (even down to n=50)

* [Feature Engineering and Selection, 2019](https://machinelearningmastery.com/handle-missing-data-python/)
* [Applied Predictive Modeling, 2013](http://appliedpredictivemodeling.com/)

## Best Papers
- [ ] [Sreehari and Nandi 2020](https://arxiv.org/pdf/2101.06218.pdf): hereafter I'll refer to it as SN20. Title: *A Machine Learning approach for classification of accretion states of
Black hole binaries*
- [ ] [Pattnaik et al. 2021](https://pure.rug.nl/ws/portalfiles/portal/157958141/staa3899.pdf): hereafter I'll refer to this paper as P21. Title: *A machine-learning approach for classifying low-mass X-ray binaries based on their compact
object nature*
- [ ] [Ingram and Motta 2020](https://arxiv.org/pdf/2001.08758.pdf): hereafter I'll refer to this paper as QPO2020. Title: *A review of quasi-periodic oscillations from black hole X-ray binaries: observation and theory*
- [x] [Cuneo et al. 2020](https://arxiv.org/pdf/2006.03074.pdf): hereafter I'll refer to this paper as Cuneo2020. Title: *A NICER look at the state transitions of the black hole candidate MAXI J1535-571 during its reflares* 

## Notes

### Astrophysics

* [Phil et al. 2019](https://ui.adsabs.harvard.edu/abs/2019HEAD...1711122U/abstract)
    * September-October 2017 NICER observed the source as it transitioned through its intermediate state
    * During this transition, the source showed a "strong low-frequency (LF) QPO which varied in frequency between 1.7 and 9.5 Hz"
    * > currently favored model for the LF QPO is that it is associated with general relativistic precession of the innermost hot-flow or corona, and therefore probes the emission and dynamics in the strongest-gravity region of the accretion flow. Spectral-timing with NICER's soft X-ray response and CCD-quality spectral resolution provides a powerful approach to test this and other models for the QPO and study the evolution of the inner disk as the QPO frequency changes. Furthermore, due to its powerful bright-source capabilities, NICER was able to sample the QPOs in MAXI J1535-571 with photon count rates more than 40 times greater than the previous best QPO spectral-timing measurements by XMM-Newton. We use these remakable data to show how the spectral-timing properties of the QPO evolve with changing frequency and use these to test the origin of the QPO and how it is connected to changes in the innermost accretion flow.

* [Huang et al. 2018: Insight and MAXIJ1545-571](https://iopscience.iop.org/article/10.3847/1538-4357/aade4c/pdf)
    * "source exhibits transitions from the low/hard state to the hard intermediate state, and eventually to the soft intermediate state."
    * QPOs are found in intermediate states
    * "energy dependence of the QPO amplitude and centroid frequency" --> but not normalization? 
    * "Assuming a geometrical origin of type-C QPOs, the source is consistent with being a high-inclination system."
    * > Black hole transients (BHTs) spend most of their lives in quiescence, and are detected during outbursts in which their spectral and timing properties change with time. During a typical outburst, they go through the low hard state (LHS), hard and soft intermediate states (HIMS, SIMS), high soft state (HSS), then again through the intermediate states and back to the LHS, following the classification given in Belloni (2010; see Remillard & McClintock 2006 for an alternative classification, and Motta et al. 2009 for a comparison). In the LHS, the X-ray spectrum can be approximately described by a power law with a spectral index of ∼1.6 (2–20 keV band), and an exponential cutoff at ∼100 keV. This hard X-ray emission is thought to arise from the Comptonization of soft disk photons in a hot corona
    * "One of the promising scenarios for type-C QPOs is that the oscillations are produced by Lense–Thirring precession of the inner accretion flow (Ingram et al. 2009)"
    * MAXIJ1535-571 was independently discovered by MAXI/GSC and SWIFT/Bat
    * "background-subtracted and dead-time-corrected" sound a lot better than what I talk about in the paper. 
    * **question:** should we use coherance parameter `Q(=ν/FWHM)`? 
    * "LFQPOs, consisting of three types (type-A, -B, and -C), are observed in the range 1.78–13.88 Hz"
    * I wonder if I should test a model that just predicts fundamental QPO properties first ... 
    * "Type-B QPOs are usually detected when a source experiences a rapid transition to the SIMS"
    * "A correlation of type-B QPO frequencies with the power-law flux has been reported by Motta et al. (2011) and Gao et al. (2017)"
    * "Jet ejections are thought to be associated with type-B QPOs and the X-ray flux peak"
    * "The correlation between the centroid frequency of QPOs and the photon energy shows three different shapes: flat, positive, and “arch”-like."
        * See Figure 11. in their paper

### Machine Learning

* [Applied Predictive Modeling, 2013](http://appliedpredictivemodeling.com/)
    * "… missing data can be imputed. In this case, we can use information in the training set predictors to, in essence, estimate the values of other predictors."
        * JBL says you can use "A constant value that has meaning within the domain, such as 0, distinct from all other values, a value from another randomly selected record; a mean, median or mode value for the column; a value estimated by another predictive model."
        
* [Feature Engineering and Selection, 2019](https://machinelearningmastery.com/handle-missing-data-python/)
    * "Many popular predictive models such as support vector machines, the glmnet, and neural networks, cannot tolerate any amount of missing values."
    * "Missing values are common occurrences in data. Unfortunately, most predictive modeling techniques cannot handle any missing values. Therefore, this problem must be addressed prior to modeling."
    * "When a predictor is discrete in nature, missingness can be directly encoded into the predictor as if it were a naturally occurring category."
    * "The simplest approach for dealing with missing values is to remove entire predictor(s) and/or sample(s) that contain missing values."
