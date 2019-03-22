// import org.apache.commons.math3.linear.RealMatrix;
// import org.apache.commons.math3.linear.MatrixUtils;
// import java.io.Serializable;

public class Quaternion {

    public static final double SINGULARITY_NORTH_POLE = 0.49999;

    public static final double SINGULARITY_SOUTH_POLE = -0.49999;

    private final double w, x, y, z;


    public  Quaternion(double w, double x, double y, double z) {
        this.w = w;
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public  double toRoll() {
        // // This is a test for singularities
        // double test = x*y + z*w;

        // // // Special case for north pole
        // // if (test > SINGULARITY_NORTH_POLE)
        // //     return 0;

        // // // Special case for south pole
        // // if (test < SINGULARITY_SOUTH_POLE)
        // //     return 0;

        // return Math.atan2(
        //             2*x*w - 2*y*z,
        //             1 - 2*x*x - 2*z*z
        //         );


        double sinr_cosp = +2.0 * (w * x + y * z);
        double cosr_cosp = +1.0 - 2.0 * (x * x + y * y);
        return Math.atan2(sinr_cosp, cosr_cosp);
    }

    public  double toPitch() {
        // This is a test for singularities
        // double test = x*y + z*w;

        // // // Special case for north pole
        // // if (test > SINGULARITY_NORTH_POLE)
        // //     return Math.PI/2;

        // // // Special case for south pole
        // // if (test < SINGULARITY_SOUTH_POLE)
        // //     return -Math.PI/2;

        // return Math.asin(2*test);
        double sinp = +2.0 * (w * y - z * x);
        if (Math.abs(sinp) >= 1)
            return Math.copySign(Math.PI / 2, sinp); // use 90 degrees if out of range
        else
            return Math.asin(sinp);
    }

    public  double toYaw() {
        // This is a test for singularities
        // double test = x*y + z*w;

        // // Special case for north pole
        // if (test > SINGULARITY_NORTH_POLE){
        //     System.out.println("aaaaaaa");
        //     return 2 * Math.atan2(x, w);}


        // // Special case for south pole
        // if (test < SINGULARITY_SOUTH_POLE){
        //     System.out.println("bbbbbbbb");
        //     return -2 * Math.atan2(x, w);}

        // return Math.atan2(
        //             2*y*w - 2*x*z,
        //             1 - 2*y*y - 2*z*z
        //         );
        double siny_cosp = +2.0 * (w * z + x * y);
        double cosy_cosp = +1.0 - 2.0 * (y * y + z * z);
        return Math.atan2(siny_cosp, cosy_cosp);
    }


    @Override
    public  String toString() {
        return "Q[" + toRoll() + "," + toPitch() + "," + toYaw() + "]";
    }
}
