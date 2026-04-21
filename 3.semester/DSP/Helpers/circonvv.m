function [ y ] = circonvv(x1,x2,N )
%the function circonv calculates the N-point circular convolution of 2 signals x1
%and x2. 
%The input vectors x1 and x2 are row vectors of of lengths <=N.
%The output y is a row vector of length N.


close all
% Check for length(x1)<=N
if length(x1)>N
    error('the length of x1 must be <=N')
end

% Check for length(x2)<=N
if length(x2)>N
    error('the length of x2 must be <=N')
end

x1=[x1 zeros(1,N-length(x1))]; % extend if nescesary the length of x1 to N
x2=[x2 zeros(1,N-length(x2))]; % extend if nescesary the length of x2 to N
m=[0:N-1]; % shift index vector
H=zeros(N,N);
x2rev=x2(mod(-m,N)+1);

for n=1:N
H(n,:)=circularshift1(x2rev,n-1,N);
end

y=x1*H';
n=0:N-1;
stem(n,y,'filled','r');

