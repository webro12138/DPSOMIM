

# SANREMO2016FINAL MULTIPLEX SOCIAL NETWORK

###### Last update: 1 Jan 2020
 
### Reference and Acknowledgments

This README file accompanies the dataset representing the multiplex social network of users in Twitter.
If you use this dataset in your work either for analysis or for visualization, you should acknowledge/cite the following paper:
	
	'Unraveling the Origin of Social Bursts in Collective Attention'
	M. De Domenico, E. G. Altmann 
	Scientific Reports 2020 10, 4629

that can be found at the following URL:

<https://www.nature.com/articles/s41598-020-61523-z>

This work has been partially supported by Max Planck Institute for the Physics of Complex Systems (Visitors program 2016) and the University of Sydney bridging Grant G199768. The data set has been built at the [CoMuNe Lab](https://comunelab.fbk.eu/). 


### Description of the dataset

We consider different types of social relationships amoung users, obtained from Twitter during an exceptional event. In this specific dataset we focused on [Sanremo Music Festival Final](https://en.wikipedia.org/wiki/Sanremo_Music_Festival) in 2016.

The multiplex network used in the paper makes use of 3 layers, corresponding to retweet, mentions and replies observed between


    Start: 2016-02-13
    End: 2016-02-13

There are 56,562 nodes, labelled with integer ID between 1 and 56,562 and 461,838 connections.
The multiplex is directed and weighted (obtained by summing up the number of a specific type of interaction over time), stored as edges list in the file

    Sanremo2016_final_multiplex.edges

with format

    layerID nodeID nodeID weight

The IDs of all layers are stored in

    Sanremo2016_final_layers.txt

The IDs of nodes (note that screen names are not provided for privacy reasons) can be found in the file

    Sanremo2016_final_nodes.txt


In addition, online interactions of users are provided with the temporal information in the file

    Sanremo2016_final_activity.txt

with format

    nodeID nodeID timestamp type

where timestamp is in seconds and type is the layer name. 

Note 1: the direction of links depends on the application, in general. For instance, if one is interested in building a network of how information flows, then the direction of RT should be reversed when used in the analysis. Nevertheless, the choice is left to the researcher and his/her own interpretation of the data, whereas we just provide the observed actions, i.e., who retweets/mentions/replies/follows whom.

Note 2: users mentioned in retweeted tweets are considered as mentions. For instance, if @A retweets the tweet 'hello @C @D' sent by @B, then the following links are created: @A @B timeX RT, @A @C timeX MT, @A @D timeX MT, because @C and @D can be notified that they have been mentioned in a retweet. Similarly in the case of a reply. If for some reason the researcher does not agree with this choice, he/she can easily identify this type of links and remove the mentions, for instance.


### License

This SANREMO2016FINAL MULTIPLEX SOCIAL NETWORK is made available under the Open Database License: <http://opendatacommons.org/licenses/odbl/1.0/>. Any rights in individual contents of the database are licensed under the Database Contents License: <http://opendatacommons.org/licenses/dbcl/1.0/>

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
	CoMuNe Lab, Fondazione Bruno Kessler 
	Trento (Italia)

email: <mdedomenico@fbk.eu>

web: <https://comunelab.fbk.eu/manlio>

