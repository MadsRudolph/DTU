
#include <gsl/gsl_fit.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SAMPLES 11
#define DATASETS 4
#define SIZE 80 

int slopes[20];
int intercepts[39];

int runplot() {
   /* The rest of this program sends gnuplot commands to the gnuplot 
      application. You can send commands from one application to another 
      via an operating system capability known as a pipe. In particular,
      a pipe enables output from one running application to be passed to 
      another. In macOS and Linux, you "open a pipe" using the nonstandard 
      popen function (short for "pipe open") from the <stdio.h> header. In 
      Windows, the function's name is _popen. The popen and _popen functions
      each receive two arguments. The first is a command for the operating 
      system to execute and the second is a file-open mode. Similar to file
      I/O, popen and _popen enable bytes to be written to or read from
      another application. This following function call launches the gnuplot
      application and opens a pipe to it through which we can write ("w"), 
      enabling this application to send bytes to gnuplot. */
   FILE *pipe = _popen("gnuplot.exe -persist'" , "w");

   // Ensure that the pipe opened successfully; if not, terminate.
   if (pipe == NULL) { 
      printf("Unable to open gnuplot\n"); 
      exit(0); 
   } 
   
   // Send commands to Gnuplot
    fprintf(pipe, "set title 'Example Plot'\n");
  //  fprintf(pipe, "plot sin(x)\n");

   
   /* Once you open the pipe, you can use standard file-processing  
      functions, such as fprintf, to send text commands to gnuplot through 
      the pipe. You simply use the pipe's FILE pointer as the output 
      destination for each command. */

   /* gnuplot can read data from a text file, such as anscombe.csv, and plot
      the data. gnuplot's "set datafile separator" command specifies the
      separator character used to separate the columns in each data row. 
      In this example, we use CSV data, so the separator is a comma. 
      Each gnuplot command you send through the pipe should end with a 
      newline character, which tells gnuplot to execute that command. */
    fprintf(pipe, "set datafile separator ','\n");

   /* gnuplot's "set terminal" command specifies the output file format
      and configuration. The command's arguments

         png size 1600,900 font ',30'

      indicate that we will output plots as PNG format images that are 1600
      pixels wide and 900 pixels tall, using gnuplot's default font in 30pt 
      size to label the plots. You could specify a custom font before the 
      comma in ',30'. */
   fprintf(pipe, "set terminal png size 1600,900 font ',30'\n");

   /* gnuplot's "set pointsize" command sets the size of the points (dots)
      displayed on the plot. The default pointsize is 1. */
   fprintf(pipe, "set pointsize 5\n");

   /* gnuplot's "set nokey" command indicates that the plot should 
      not have a key describing the meaning of various plot elements. */
   fprintf(pipe, "set nokey\n");

   /* gnuplot's "set xrange" command sets the x-axis range. In this example,
      we set every plot's x-axis range from 2 through 20 so all the plots
      have identical x-axes. */
 
     fprintf(pipe, "set xdata time\n");  // Specify that x-axis data is time
    fprintf(pipe, "set timefmt \"%%Y-%%m-%%d %%H:%%M:%%S\"\n");  // Input time format in your data
    fprintf(pipe, "set format x \"%%H:%%M\"\n");  // Display format for x-axis (e.g., HH:MM)
   
  fprintf(pipe, "set grid\n");
     fprintf(pipe, "set xlabel 'Time'\n");
    fprintf(pipe, "set ylabel 'Data'\n");
   /* gnuplot's "set yrange" command sets the y-axis range. In this example,
      we set every plot's y-axis range from 2 through 14 so all the plots
      have identical y-axes. Setting both the x- and y-axes identically
      for all four plots ensures that all the dots and regression lines
      are plotted using the same scale. This will enable you to see that 
      the regression lines appear to be identical. */
    fprintf(pipe, "set yrange [30:60] \n");

   // The following loop produces the four plots
   // for (int i = 1; i <= DATASETS; ++i) {
      // gnuplot's "set title" command sets the title above the plot
      fprintf(pipe, "set title 'Dataset'\n");

      /* gnuplot's "set output" command sets the PNG image's filename
         in which the plot will be stored. */
      fprintf(pipe, "set output 'dataset.png'\n");

      /* gnuplot's "plot" command creates a plot. The following is a sample
         plot command sent to gnuplot when the fprintf below executes:

            plot 'anscombe.csv' using 1:2 with points pointtype 7, 0.5*x+3.0 linewidth 3 linecolor rgb 'red'

         The following are the plot command's arguments:

         'anscombe.csv' 
            The file containing the data to plot.

         using %d:%d 
           Specifies the start and end column numbers to plot. We substitute
           integer values for the two %d specifiers. For example, 0:1 
           indicates that the x-y coordinates for the plot are in columns 0 
           and 1 of anscombes.csv.

         with points 
           Gnuplot will display individual x-y data points.

         pointtype 7, 
           Points are displayed using gnuplot point type 7 (circular dots).

         %f*x+%f
           This is the calculation mx + b that is used to calculate the 
           regression line's points. The first %f is replaced with the 
           slope (m) and the second %f is replaced with the intercept (b).

         linewidth 3
           Specifies the regression line's thickness should be 3pt.

         linecolor rgb 'red' 
           Specifies that lines should be displayed in red.

         Note that the two strings in the fprintf below are concatenated
         by the compiler because they are separated only by whitespace.
      */
      fprintf(pipe, "plot 'data.csv' using 1:2 with points pointtype 7 title 'Dataset'\n");  //
        // "pointtype 7, %f*x+%f linewidth 3 linecolor rgb 'red'\n");//, 
        // i * 2 - 1, i * 2, slopes[i], intercepts[i]);
 //  }

   // Close the pipe to terminate the connection to gnuplot. 
   // Close the pipe

    if (_pclose(pipe) == -1) {
        perror("pclose failed");
        return 1;
    }
  return 0;
}

/**************************************************************************
 * (C) Copyright 1992-2021 by Deitel & Associates, Inc. and               *
 * Pearson Education, Inc. All Rights Reserved.                           *
 *                                                                        *
 * DISCLAIMER: The authors and publisher of this book have used their     *
 * best efforts in preparing the book. These efforts include the          *
 * development, research, and testing of the theories and programs        *
 * to determine their effectiveness. The authors and publisher make       *
 * no warranty of any kind, expressed or implied, with regard to these    *
 * programs or to the documentation contained in these books. The authors *
 * and publisher shall not be liable in any event for incidental or       *
 * consequential damages in connection with, or arising out of, the       *
 * furnishing, performance, or use of these programs.                     *
 **************************************************************************/

/**************************************************************************
* (C) Copyright 1992-2021 by Deitel & Associates, Inc. and               *
* Pearson Education, Inc. All Rights Reserved.                           *
*                                                                        *
* DISCLAIMER: The authors and publisher of this book have used their     *
* best efforts in preparing the book. These efforts include the          *
* development, research, and testing of the theories and programs        *
* to determine their effectiveness. The authors and publisher make       *
* no warranty of any kind, expressed or implied, with regard to these    *
* programs or to the documentation contained in these books. The authors *
* and publisher shall not be liable in any event for incidental or       *
* consequential damages in connection with, or arising out of, the       *
* furnishing, performance, or use of these programs.                     *
**************************************************************************/

int main(){
   runplot();
while(1){


}

}