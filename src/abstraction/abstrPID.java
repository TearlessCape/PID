package abstraction;

public abstract class abstrPID {

    //Constants

    //Variables
    protected double

        period,

        kP = 0.0,
        kI = 0.0,
        kD = 0.0,

        error = 0.0,
        errorInt = 0.0,
        errorDeriv = 0.0,

        setpoint = 0.0,
        tolerance = 0.0;

    //Constructors
    public abstrPID(double period) {this.period = period; configure();}

    //Getters
    public double getPeriod() {return period;}
    public double getP() {return kP;}
    public double getI() {return kI;}
    public double getD() {return kD;}
    public double getError() {return error;}
    public double getErrorInt() {return errorInt;}
    public double getErrorDeriv() {return errorDeriv;}
    public double getSetpoint() {return setpoint;}
    public double getTolerance() {return tolerance;}

    //Setters
    public void setP(double kP) {this.kP = kP;}
    public void setI(double kI) {this.kI = kI;}
    public void setD(double kD) {this.kD = kD;}
    public void setSetpoint(double setpoint) {this.setpoint = setpoint;}
    public void setTolerance(double tolerance) {this.tolerance = tolerance;}

    //Resetters
    public void resetError() {error = 0;}
    public void resetErrorInt() {errorInt = 0;}
    public void resetErrorDeriv() {errorDeriv = 0;}

    //Main
    public boolean atSetpoint(double error) {return Math.abs(error) <= tolerance;}

    //Helper
    protected double calcError(double processVariable) {return setpoint - processVariable;}

    //Abstractions
    public abstract double calculate(double processVariable);
    public abstract void configure();

}