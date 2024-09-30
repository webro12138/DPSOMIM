

# HUMAN MICROBIOME MULTIPLEX NETWORK

###### Last update: 12 July 2022

### Reference and Acknowledgments

This README file accompanies the dataset representing the multiplex microbiome network.
If you use this dataset in your work either for analysis or for visualization, you should acknowledge/cite the following papers:

	“Dynamics and associations of microbial community types across the human body”
	T. Ding and P. Schloss
	Nature 2014 509, 357–360 


	
	“Spectral Entropies as Information-Theoretic Tools for Complex Network Comparison”
	M. De Domenico and J. Biamonte
	Physical Review X 2016 6, 041062


that can be found at the following URLs:

<https://www.nature.com/articles/nature13178>

<https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.041062>


### Description of the dataset

We consider different types of microbial communities across the human body, building an interaction network for each of 18 distinct human body sites. We have elaborated the resulting network from the original work by Ding and Schloss (see above).

The multiplex network used in the paper makes use of the following layers:

1. Anterior_nares
2. Buccal_mucosa
3. Hard_palate
4. Keratinized_gingiva
5. L_Antecubital_fossa
6. L_Retroauricular_crease
7. Mid_vagina
8. Palatine_Tonsils
9. Posterior_fornix
10. R_Antecubital_fossa
11. R_Retroauricular_crease
12. Saliva
13. Stool
14. Subgingival_plaque
15. Supragingival_plaque
16. Throat
17. Tongue_dorsum
18. Vaginal_introitus


There are 305 nodes, labelled with integer ID between 1 and 305, and 4433 connections.
The multiplex is undirected and unweighted, stored as edges list in the file
    
    HumanMicrobiome_multiplex.edges

with format

    layerID nodeID nodeID weight

(Note: weight is 1 for all edges)

The IDs of all layers are stored in 

    HumanMicrobiome_layers.txt

The IDs of nodes, together with their name can be found in the file

    HumanMicrobiome_nodes.txt



### License

This HUMAN MICROBIOME MULTIPLEX NETWORK DATASET is made available under the Open Database License: <http://opendatacommons.org/licenses/odbl/1.0/>. Any rights in individual contents of the database are licensed under the Database Contents License: <http://opendatacommons.org/licenses/dbcl/1.0/>

You should find a copy of the above licenses accompanying this dataset. If it is not the case, please contact us (see below).

A friendly summary of this license can be found here:

<http://opendatacommons.org/licenses/odbl/summary/>

and is reported in the following.

======================================================
ODC Open Database License (ODbL) Summary

This is a human-readable summary of the ODbL 1.0 license. Please see the disclaimer below.

You are free:

*    To Share: To copy, distribute and use the database.
*    To Create: To produce works from the database.
*    To Adapt: To modify, transform and build upon the database.

As long as you:
    
*	Attribute: You must attribute any public use of the database, or works produced from the database, in the manner specified in the ODbL. For any use or redistribution of the database, or works produced from it, you must make clear to others the license of the database and keep intact any notices on the original database.
    
*	Share-Alike: If you publicly use any adapted version of this database, or works produced from an adapted database, you must also offer that adapted database under the ODbL.
    
*	Keep open: If you redistribute the database, or an adapted version of it, then you may use technological measures that restrict the work (such as DRM) as long as you also redistribute a version without such measures.

======================================================


### Contacts

If you find any error in the dataset or you have questions, please contact

	Manlio De Domenico
	University of Padua
	Padua (Italy)

email: <manlio.dedomenico@unipd.it>web: <https://manliodedomenico.com/>