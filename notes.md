Political leaning predicting system.

+ An overall look at the project would show:
	+ A front-end:
		+ Design:
			+ Either a full website, with embedded FB/Twitter widgets
			+ Or an API, if it turns out to be a lot of work:
				+ The API would only need a single endpoint:
                        	+ The endpoint could accept POST requests
                        		+ Such as www.mywebsite.com/predict
                              	+ And would take the tweet or FB-post url, in the request's body
                              + Or accept GET requests
                              	+ And would take the tweet/FB-post url as url parameters
                                    + Such as www.mywebsite.com/predict?post_url=https://twitter.com/realDonaldTrump/status/743078235408195584
		+ Functionality:
			+ The front-end would capture the user input, and pass it to the backend.
			+ The expected input would be a FB post / Twitter post url.
			+ The front-end would show/return the result of the backend's processing:
			+ The result would contain: 
				+ The text content of the TW/FB post
				+ The predicted political leaning of the post
				+ The confidence of the prediction
	+ A back-end:
		+ At the heart of the back-end we'd have a machine learning trained model.
		+ The back-end would:
			+ Take a post's url, and access it
			+ Obtain its text content
			+ Feed the text content to the machine learning model
			+ Expect a political leaning prediction and prediction's confidence from the machine learning model
			+ Return the result to the front-end
	+ The toolchain. This project would require some additional tools:
		+ Some code to obtain posts from a particular FB/TW user.
            	+ This would use the TW/FB APIs
			+ These posts would be used to train the machine learning model
			+ The targeted users would most likely be known left/right wing public figures
			+ This would probably be split between two different tools:
				+ Twitter-posts obtaining tool
				+ And FB-posts obtaining tool
			+ The text content of these posts could be labeled with their political leaning, according to the author, and stored in a database,
                  to train the ML model later
		+ Some code to train the machine learning model, with the data obtained from public figures' posts
            + optional: some code to pickle (store in hard drive) the trained models. To be able to have differently trained models, and be able to
            change the one we're using in the backend