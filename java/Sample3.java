import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.BufferedWriter;


public class Sample3 {
  public static void main(String args[]){

    try {
      File f = new File("sample3.csv");
      BufferedReader br = new BufferedReader(new FileReader(f));
      double w = 0;
      double x = 0;
      double y = 0;
      double z = 0;
      int length = 583;
      String[][] data = new String[length][4];
      double[][] quat = new double[length][3];
        FileWriter t = new FileWriter("sample5.csv", false);
        PrintWriter p = new PrintWriter(new BufferedWriter(t));
      String line = br.readLine();
      for (int row = 0; line != null; row++) {
        data[row] = line.split(",", 0);
        // System.out.println(line);
        line = br.readLine();
      }
      br.close();

      // CSVから読み込んだ配列の中身を表示
      for(int row = 0; row < length; row++) {
        for(int col = 0; col < 4; col++) {
            System.out.println(data[row][col]);
            switch (col) {
            case 0:
                int ww = Integer.parseInt(data[row][col]);
                w = (double)ww;
                break;
            case 1:
                int xx = Integer.parseInt(data[row][col]);
                x = (double)xx;
                break;
            case 2:
                int yy = Integer.parseInt(data[row][col]);
                y = (double)yy;
                break;
            case 3:
                int zz = Integer.parseInt(data[row][col]);
                z = (double)zz;
                break;
            default:
                System.out.println("エラー");
            }
        }
        double sum = w*w + x*x + y*y + z*z;
        double a = Math.sqrt(sum);
        // System.out.println(a);
        w = w/a;
        x = x/a;
        y = y/a;
        z = z/a;
        // double[] q1 = new double[4];
        Quaternion q1 = new Quaternion(w, y, x, z);
        // double roll = -Math.toDegrees(q1.toRoll());
        // double pitch = -Math.toDegrees(q1.toYaw());
        // double yaw = Math.toDegrees(q1.toPitch());
        quat[row][0] = -Math.toDegrees(q1.toPitch());
        quat[row][1] = -Math.toDegrees(q1.toRoll());
        quat[row][2] = Math.toDegrees(q1.toYaw());
        p.print(quat[row][0]);
        p.print(",");
        p.print(quat[row][1]);
        p.print(",");
        p.print(quat[row][2]);
        p.println();    // 改行
      }
      p.close();
         // System.out.println(data[0][0]);
    // for(int row = 0; row < 1767; row++) {
    //     for(int col = 0; col < 3; col++) {
    //       System.out.println(quat[row][col]);
    //     }
    // }

    // double w = 0;
    // double x = 0;
    // double y = 0;
    // double z = 0;
    // double sum = w*w + x*x + y*y + z*z;
    // double a = Math.sqrt(sum);
    // System.out.println(a);
    // w = w/a;
    // x = x/a;
    // y = y/a;
    // z = z/a;
    // // double[] q1 = new double[4];
    // Quaternion q1 = new Quaternion(w, x, y, z);
    // double roll = -Math.toDegrees(q1.toRoll());
    // double pitch = -Math.toDegrees(q1.toYaw());
    // double yaw = Math.toDegrees(q1.toPitch());
    // System.out.println(roll);
    // System.out.println(pitch);
    // System.out.println(yaw);

    } catch (IOException e) {
      System.out.println(e);
    }
  }
}


