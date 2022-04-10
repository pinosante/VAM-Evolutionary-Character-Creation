# VAM-Evolutionary-Character-Creation
Create beatiful girls, guys and futas using a sophisticated genetic algorithm.

Hi everyone, this is an upgrade from my VAM Character Fusion project, with a lot of amazing features.

# What does this do?
This app allows you to:
1.	Scan all your appearances
2.	Create a "blue print" of your favorite appearance type based on your appearances. 
3.	Sample 20 apperances based on your personal blueprint.
4.	Vote on these appearances.
5.	Generate another 20 appearances based on your voting.
6.	Keep repeating this until you have an appearance which is beautiful.
It's basically a "hot or not" app, based on your preferences!

# So how do I use this? (Quick Start)
The fastest way to get results, is to:
1.	Open the VAM Evolutionary Character Creation app (Windows Executable)
2.	Go to Step 1 (in the app) and select your VAM Folder (the folder which contains VAM.exe)
3.	Go to Step 2 and select a female (or male/futa) template from your Appearances directory
4.	Go to Step 3 and select "All appearances"
5.	Go to Step 5 and select "Gaussian Samples" if you have 20 or more appearances found in Step 4; if you have less, choose "Random Crossover"
6.	Press "Initialize Population"
7.	Open VAM and open the VAM Evolutionary Character Creation Companion save
8.	In VAM click on 1 to 20 to look at the generated appearances
9.	In the app (windows executable), rate the corresponding 1-20 appearances
10.	Press Generate Population after you have rated them all
11.	Go to 8 and keep repeating until you're satisfied with the generated appearances
12.	Save your favorite appearance to a new file.

# So how do I use this? (Detailed Explanation)
1.	When you start the app, click on the "Appearance Dir" button and select your Virt-A-Mate directory, the folder where your VAM.exe is located.
2.	Select a Child Template Appearance by clicking on either the Female, Male or Futa button. Then select the matching Appearance you want to use as a Child Template. The generated children will have the skin and look of this Appearance. You can use + - to change the amount of thumbnails per row. You can also use a file filter.
3.	Choose the source of the Parents for the App.
  0.	All Appearances: all the appearances in the Appearance Dir matching the Child Template will be used as Parents.
  1.	All Favorited Appearances: only the favorited appearances in the Appearance Dir matching the Child Template will be used as Parents.
  2.	Choose Files: hand pick which appearances you want to use as parents, but pick at least two parents.
4.	Look at the information in Step 4, and make sure that you have at least two appearances available as parents. If not, go back to step 3.
5.	Choose your initialization method.
  0.	Gaussian Sample: this is a fancy mathematical way of finding the "mean" of all the files in your selection from step 3, which also takes into account the correlations between all variables. In simple speak: it tries to capture the "mean flavour" of your appearances and then picks Children randomly from this flavour pool. Note: this initialization can take a while, but this is only for the first generation. If you want to use this properly, you need a lot of appearances (20+) to make a good estimate of the "mean".
  1.	Random Crossover: at random, two parents are chosen every time to create a child. This is a fast process but has more variance in the created children. If you have few appearances/parents, this should be the method to use.
6.	Optional: set any of the three options, but I strongly advise to set option B).
  0.	A) Removing morphs below a certain treshold. This is to "ignore" morphs which have very low values. Some appearances have 500 morphs, with many of them very small values. By setting a treshold, only the meaningful ones with values larger than your treshold, are kept.
  1.	B) This app does not work well when you use appearances which have one morph which stores the complete character. To filter these out, I recommend settings a minimal morph count of about 150. This way, only appearances which have more than 150 morphs are selected. Since appearances with a single morph for the whole character rarely have more than 150 morphs in total, this will effectively ignore them.
  2.	C) By default the children created by this app will not be selectable in the app. This would clutter the filedialog with 20 children every time you open it. If you are happy with a generated child, just save it as a new appearance with a custom name if you want to be able to select it again in this app as a parent. If you still want to see your children when you open the file selection dialogs, set this to Yes.
7.	Press "Initialize Population". If you use Gaussian Samples, this will take a while (~1 minute).
8.	Rate Children. You now see Generation 1 of your 20 children. Each child is a new generated appearance based on your previous choices. I made a "VAM Evolutionary Character Creation Companion" save which you can open in VAM. This save helps with the rating process. When you open this save in VAM, you can click on one of the 20 numbers to the left, to see each of the generated appearances by the python app. And then rate them in the python app. I have both VAM and the python app open with the windows next to eachother. The higher you rate each child, the bigger the chance that it will be used to create children for the next generation. The highest rated appearance (or in the case of a tie, the first child with that rating), will always be kept and stored as Child 1 for the new generation.
9.	Generate Next Population. If you're done with rating, you can press the Generate Next Population. 
10.	Return to Step 8. You can keep doing this until you are happy with the results.
11.	When you are happy with one of the generated children, make sure to save that appearance to a custom name. If you rerun the app, all cihldren appearances will be overwritten, so better save it to a new one.
How did you make this app?
I made the app in python. The source code is available on github: https://github.com/pinosante/VAM-Evolutionary-Character-Creation. If you see anything which can be improved, please let me know! I'm not a programmer by trade (as you can probably tell by looking at the source code :) ).

# How does the rating work?
After all characters are rated a roulette wheel selection takes place. This means that each character's rating gets a slice on a roulettewheel based on their rating. The higher the rating, the bigger the slice. To be precise: a child with a rating of 3, will have 3 times more chance to be chosen as a future parent, than a child with a rating of 1. After assigning all the slices on the roulettewheel, the app will spin this roulettewheel every time a parent needs to be chosen. This happens 40 times, since for each new child, two parents have to be chosen. Using this roulettewheel will effectively make sure that the appearances you rated highest, will be more often chosen as parents, resulting in cihldren being generated which will look more like the ones you rated highest.

# How does your app deal with Futas?
There are different ways of defining a "futa" file, but the one I use in this app is by looking if the "MVR_G2Female" morph is in the appearance file. This seems to be a popular futa format and is easy to work with. An example of a futa like this is: https://hub.virtamate.com/resources/violet-look-futa.8977/ (But there are many more to be found on the hub). If you choose a futa as a template, you can then either choose females or other futas, as parents! The reverse is also true: if you choose a female template and there are some futa files you really like, you can use those as parents for your female template as well. The "All Appearances" / "Favorited Appearances" / "Choose Files" buttons all support this, and will always show you the matching appearances (so futa + female parents for either a female or futa template).

# Some useful tips
•	If you have very similar looking children, only rate one of them, and keep the other at 1. This way you keep the gene pool more diverse.
•	When doing the first few generations, make sure to keep the super weird/broken characters at 1 and everything which looks decently normal, at 2 (even if ugly). This way you will get rid of the weird/broken characters.
•	If there is a character which has an ugly face, but some other good features (body/look) consider still rating with a 2 or 3 to keep those body genes in the pool.
•	It is best to use a template appearance of a naked person, this loads faster and makes it easier to rate the generated appearances.
•	If the VAM Evolutionary Character Creation Companion save file is a bit slow with loading, you can try deleting the two persons at 45 and 90 degree angles, and doing a new save of this companion file to make it load faster.
•	If for some reason the app doesn't work, or stops working, go to the data directory in the app folder and delete "settings.json". This will give you a new "fresh" version of the app.
Please make my day and share what you create!
I'm really curious what you come up with, so feel free to share screenshots or var's of the looks you created with this app! Let me also know in the discussion, if the app was able to capture some of the "flavour" of your favorite appearances! This is what keeps me motivated.

# Enjoy!
