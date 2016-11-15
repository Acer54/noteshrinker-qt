The programmer uses pylupdate4 to create or update a .ts translation file for each language that the application
is to be translated into. A .ts file is an XML file that contains the strings to be translated and the corresponding
translations that have already been made. pylupdate4 can be run any number of times during development to update
the .ts files with the latest strings for translation.
The translator uses Qt Linguist to update the .ts files with translations of the strings.
The release manager then uses Qt’s lrelease utility to convert the .ts files to .qm files which are compact binary
equivalents used by the application. If an application cannot find an appropriate .qm file, or a particular
string hasn’t been translated, then the strings used in the original source code are used instead.
The release manage may optionally use pyrcc4 to embed the .qm files, along with other application resources
such as icons, in a Python module. This may make packaging and distribution of the application easier.