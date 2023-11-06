package solution;

import abstraction.abstrPID;

/*
Resources:
    Intro to PID: https://docs.wpilib.org/en/stable/docs/software/advanced-controls/introduction/introduction-to-pid.html
    Rev Closed Loop: https://docs.revrobotics.com/sparkmax/operating-modes/closed-loop-control
    PID Graph: https://www.desmos.com/calculator/9co6bzatzc
*/

public class TemplatePID extends abstrPID {

    public TemplatePID(double period) {super(period);}
    public double calculate(double processVariable) {return 0.0;}
    public void configure() {}

}