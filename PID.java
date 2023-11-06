//To use this solution...
//  If there is a PID.java in the solution folder, rename/delete it
//  Move this file to the solution folder

package solution;

import abstraction.abstrPID;

public class PID extends abstrPID {

    public PID(double period) {super(period);}

    public double calculate(double processVariable) {

        double newError = calcError(processVariable);
        double errorDelta = newError - error;

        error = newError;
        errorInt += period * (newError + error) / 2;
        errorDeriv = errorDelta / period;

        return kP * error + kI * errorInt + kD * errorDeriv;

    }

    public void configure() {

        setP(500);
        setI(150);
        setD(100);

    }
    
}