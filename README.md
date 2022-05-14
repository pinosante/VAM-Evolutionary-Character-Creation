# VAM-Evolutionary-Character-Creation
Create beautiful girls, guys and futas using a sophisticated genetic algorithm.

Hi everyone, this is an upgrade from my VAM Character Fusion project, with a lot of amazing features.

# What does this do?
This app allows you to:
1.	Scan all your appearances
2.	Create a "blueprint" of your favorite appearance type based on your appearances. 
3.	Sample 20 appearances based on your personal blueprint.
4.	Vote on these appearances.
5.	Generate another 20 appearances based on your voting.
6.	Keep repeating this until you have an appearance which is beautiful.
It's basically a "hot or not" app, based on your preferences!

# So how do I use this? (Quick Start)
The fastest way to get results, is to:
1.	Open the VAM Evolutionary Character Creation app (Windows Executable)
2.	Go to Step 1 (in the app) and select your VAM Folder (the folder which contains VAM.exe)
3.	Go to Step 2 and select your Appearance directory
4.	Go to Step 3 and select a female (or male/futa) template from your Appearances directory
5.	Go to Step 4 and select "All appearances"
6.	Go to Step 6 and select "Gaussian Samples" if you have 20 or more appearances found in Step 4; if you have less, choose "Random Crossover"
7.	Press "Initialize Population"
8.	Open VAM and open the VAM Evolutionary Character Creation Companion save
9.	In VAM click on "Connect to App"
10.	In VAM rate the corresponding 1-20 appearances
11.	In vAM click on Generate Population after you have rated them all
12.	Go to 8 and keep repeating until you're satisfied with the generated appearances
13.	Save your favorite appearance to a new file.

# So how do I use this? (Detailed Explanation)
1.	When you start the app, click on the "Appearance Dir" button and select your Virt-A-Mate directory, the folder where your VAM.exe is located.
2.	After that, choose an Appearance folder by clicking on it. This folder can be located wherever you want.
3.	Select a Child Template Appearance by clicking on either the Female, Male or Futa button. Then select the matching Appearance you want to use as a Child Template. The generated children will have the skin and look of this Appearance. You can use + - to change the amount of thumbnails per row. You can also use a file filter.
4.	Choose the source of the Parents for the App.
    1.	All Appearances: all the appearances in the Appearance Dir matching the Child Template will be used as Parents.
    2.	All Favorited Appearances: only the favorited appearances in the Appearance Dir matching the Child Template will be used as Parents.
    3.	Choose Files: hand pick which appearances you want to use as parents, but pick at least two parents.
5.	Look at the information in Step 4 (in the app), and make sure that you have at least two appearances available as parents. If not, go back to the previous step here.
6.	Choose your initialization method.
    1.	Gaussian Sample: this is a fancy mathematical way of finding the "mean" of all the files in your selection from step 3, which also takes into account the correlations between all variables. In simple speak: it tries to capture the "mean flavour" of your appearances and then picks Children randomly from this flavour pool. Note: this initialization can take a while, but this is only for the first generation. If you want to use this properly, you need a lot of appearances (20+) to make a good estimate of the "mean".
    2.	Random Crossover: at random, two parents are chosen every time to create a child. This is a fast process but has more variance in the created children. If you have few appearances/parents, this should be the method to use.
7. Optional: set any of the options, but I strongly advise to set option B).
    1. A) Removing morphs below a certain threshold. This is to "ignore" morphs which have very low values. Some appearances have 500 morphs, with many of them very small values. By setting a threshold, only the meaningful ones with values larger than your threshold, are kept.
    2. B) This app does not work well when you use appearances which have one morph which stores the complete character. To filter these out, I recommend settings a minimal morph count of about 150. This way, only appearances which have more than 150 morphs are selected. Since appearances with a single morph for the whole character rarely have more than 150 morphs in total, this will effectively ignore them.
    3. C) This setting determines how many 'elite' (highest rated) looks the app will keep from the old generation when generating a new generation. Only looks with the highest rating you selected will be kept. So for example: let's say you set this option to 3 and the highest rating you have given your looks is a "5". If you rated 10 of your looks with a "5", this option will result in keeping the first 3 children with a rating of "5" for the next generation. By default this option is set to 1, to make sure that only 1 of the highest rated children is kept for the next generation. You can also set this to 20 if you want to keep all looks of the highest rating you give. A word of caution though: this decreases the genetic diversity of your gene pool. Simply put: it's best to keep this option below 3 in general.
    4. D) If you want to be able to automatically scan subdirectories of your appearance folder for appearances as well, set this to Yes.
8. Press "Initialize Population". If you use Gaussian Samples, this will take a while (~1 minute).
9. The app will now show a window asking you to open the "VAM Evolutionary Character Creation Companion" save. Open the save and click on "Connect to App". From here on, you can do everything in VAM.
10. Rate Children. You can click on one of the 20 numbers to the left, to see each of the generated appearances by the python app. You can click on a rating from 1 to 5. The higher you rate each child, the bigger the chance that it will be used to create children for the next generation. By default, the highest rated appearance, called the 'elite', (or in the case of a tie, the first child with that rating), will always be kept and stored as Child 1 for the new generation. You can increase the amount of elites to be automatically saved for the next generation in the options, by changing "Max kept elites (highest rated):" to a number higher than 1. One word of caution though: if you keep too many elites, this will hurt the diversity of your gene pool. In simple words: keep this number low (below 3 or so).
11. Generate Next Population. If you're done with rating, you can press the button 'Generate Next Population'. 
12. Return to Step 10. You can keep doing this until you are happy with the results.
13. When you are happy with one of the generated children, make sure to save that appearance to a custom name. If you rerun the app, all children appearances will be overwritten, so better save it to a new one.

# What does "Variate Population" do?
Variate Population looks at all appearances in the Appearances directory and randomly picks 20 of them, to use as templates for the current generation. This is a cool way to see how the morphs of this current generation would look on a different appearance template.

# What does "Use current Appearance as Template" do?
You can change the appearance of the Person by loading a new appearance. Then, if you click on the "Use current Appearance as Template" button, all childs in this generation will use this appearance as a template. A nice way to use this, is to use "Variate Population" and once you see an appearance you like, click on "Use current Appearance as Template" to apply it to the whole generation.

# What does "Reset" do?
This resets the algorithm, so you start back over at generation 1. The initialization is also redone, so you'll get a fresh gene pool based on a Gaussian Sample or Crossover method (depending on your choices when starting the python app). This way you can start from scratch if you want a new gene pool, without having to quit VAM or more importantly, leave VR.

# What does "Quicksave Appearance" do?
This saves the current appearance to the "Custom/Person/Appearances/VAM Evolutionary Character Creation/Quicksaves" folder as "Quicksave #" with # a randomly generated number. Unfortunately without a thumbnail. You can use this to quickly save some appearances you like.

# How did you make this app?
I made the app in python. The source code is available on github: https://github.com/pinosante/VAM-Evolutionary-Character-Creation. If you see anything which can be improved, please let me know! I'm not a programmer by trade (as you can probably tell by looking at the source code :) ).

# How does the python app communicate with VAM?
In VAM I created some UIText atoms, which are mainly used for communication. One of these UIText Atoms is "VAM2Python" for instance. By saving a preset for this UIText Atom with a command as the actual text, the python app can read commands from VAM. The python app checks every 25 ms whether this "VAM2Python" file has been updated. Likewise, python also writes to UIText Atom files which are read by VAM. For example a text file which contains the generation number, or the RatingBlocker atom which is also updated with text by the python app to show the current progress.

# How does the rating work?
After all characters are rated a roulette wheel selection takes place. This means that each character's rating gets a slice on a roulette wheel based on their rating. The higher the rating, the bigger the slice. To be precise: a child with a rating of 3, will have 3 times more chance to be chosen as a future parent, than a child with a rating of 1. After assigning all the slices on the roulette wheel, the app will spin this roulette wheel every time a parent needs to be chosen. This happens 40 times, since for each new child, two parents have to be chosen. Using this roulette wheel will effectively make sure that the appearances you rated highest, will be more often chosen as parents, resulting in children being generated which will look more like the ones you rated highest.

# How does your app deal with Futas?
There are different ways of defining a "futa" file, but the one I use in this app is by looking if the "MVR_G2Female" morph is in the appearance file. This seems to be a popular futa format and is easy to work with. An example of a futa like this is: https://hub.virtamate.com/resources/violet-look-futa.8977/ (But there are many more to be found on the hub). If you choose a futa as a template, you can then either choose females or other futas, as parents! The reverse is also true: if you choose a female template and there are some futa files you really like, you can use those as parents for your female template as well. The "All Appearances" / "Favorited Appearances" / "Choose Files" buttons all support this, and will always show you the matching appearances (so futa + female parents for either a female or futa template).

# Some useful tips
- With this version of the app you can actually use it in VR! Make sure you start the python app first, then enter VR load the companion save and "Connect to app".
- Really make sure to set option B to a value like 150, otherwise you end up with characters based on a single morph, which will mess up the genetic algorithm.
- If you have very similar looking children, only rate one of them, and keep the other at 1. This way you keep the gene pool more diverse.
- When doing the first few generations, make sure to keep the super weird/broken characters at 1 and everything which looks decently normal, at 2 (even if ugly). This way you will get rid of the weird/broken characters.
- If there is a character which has an ugly face, but some other good features (body/look) consider still rating with a 2 or 3 to keep those body genes in the pool.
- It is best to use a template appearance of a naked person, this loads faster and makes it easier to rate the generated appearances.
- If for some reason the app doesn't work, or stops working, go to the data directory in the app folder and delete "settings.json". This will give you a new "fresh" version of the app.

# Shout out to
- Felka99 for beta testing, adding some great suggestions, looking at my code, adding some features and helping me out to do this whole github thing. Thanks a bunch!
- ypeckak/unnamedplugins for beta testing and adding some great suggestions!

# Enjoy!
Please make my day and share what you create! I'm really curious what you come up with, so feel free to share screenshots or var's of the looks you created with this app! Let me also know in the discussion, if the app was able to capture some of the "flavour" of your favorite appearances! This is what keeps me motivated.
