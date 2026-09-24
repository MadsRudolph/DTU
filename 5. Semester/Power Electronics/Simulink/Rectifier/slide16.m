xx=0:0.1:1;
e=30*pi/180;
for i=1:11
a=asin(xx(i));
func=@(x)sin(x-e)+(xx(i)/cos(e)-sin(a-e))*exp((a-x)/tan(e))-xx(i)/cos(e);
xf=fzero(func,pi)

b(i)=xf*180/pi;
% x=0:2*pi;
% f=sin(x-e)+(xx/cos(e)-sin(a-e))*exp((a-x)/tan(e))-xx/cos(e);
end
a=asind(xx);