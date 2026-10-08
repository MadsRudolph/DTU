---
course: "34870"
type: transcript
lecture: 7
source: "Slides/34870_Lecture_7_E26.mp4"
---
# Lecture 7 — transcript of the commented slides

> [!info] Machine transcript
> Whisper large-v3 (faster-whisper, GPU), English forced, vocabulary prompt. VCH speaks with a strong accent, so expect slips such as "buffer" = woofer, "pistol" = piston, "Tillis-Moll" = Thiele-Small. Timestamps are mm:ss into the video. The note: [[Lecture 7 - Moving Coil Loudspeakers]].

[00:04] Welcome to this lecture on loudspeakers. This is the first lecture on loudspeakers in the electroacoustics course is about moving coil loudspeakers.  
[00:11] This is a sketch of a moving coil loudspeaker. The moving coil loudspeaker has a diaphragm, which is attached to a coil that is bound around a former, and these are the moving parts of the loudspeaker.  
[00:27] The diaphragm and voice coil are attached to the basket, which is the frame of the loudspeaker,  
[00:34] using two parts of the so-called suspension. The suspension is formed by the spider and the  
[00:42] surround. These are elastic elements that provide compliance and some losses. The spider's mission  
[00:50] is to keep the coil inside this gap here that contains the magnetic field. The magnetic field  
[00:57] is created by the magnet and this magnetic field from the magnet is driven through the coil using  
[01:05] the polar pieces which are metallic parts. The way it works is by driving a current through the coil  
[01:11] which creates a force on the diaphragm that moves and generates sound. There are many kinds and  
[01:22] sizes of loudspeakers depending on the use. Mainly the size has to do with the frequency range the  
[01:27] loudspeaker is meant for. Some loudspeakers are meant for multi frequency, for a full range,  
[01:32] but some others are meant for low, mid or high frequencies. The low frequency loudspeakers are  
[01:37] mid-frequency mid-range, and tweeters are the high-frequency loudspeakers.  
[01:43] However, the principle is the same for all of them.  
[01:46] This is the equivalent circuit from Leech of a loudspeaker.  
[01:53] It's based on the magnetic principle, like the dynamic microphone.  
[01:58] The mechanical part looks the same.  
[02:01] This is the mass of the diaphragm, mmd, D for diaphragm,  
[02:05] and these are the elements of the suspension, the resistance and the compliance.  
[02:10] In the acoustic part we have the front and back radiation. These elements will be spelled out when we have boxes and other elements.  
[02:22] The electrical part consists of a generator with its own output impedance or resistance, and then the coil that has a resistance.  
[02:31] This would also include wires inside the coil.  
[02:35] And this coil, if modeled in more detail, is a lossy coil, so it has a resistance associated.  
[02:46] We can get some understanding of how a loudspeaker works by comparing it with a dynamic microphone.  
[02:50] If you remember, the dynamic microphone was controlled by damping, because it had a bandpass  
[02:58] frequency response, and its voltage depends on the velocity.  
[03:08] For a loudspeaker, the parameter to be measured is the sound pressure and the distance, that is what the loudspeaker should produce.  
[03:15] And that can be estimated by considering the loudspeaker as a point source on a plane or a buffer.  
[03:22] In this case, we have the expression for a point source, but multiplied by 2, that means that instead of a 4, we have a 2 here, because it is on a plane.  
[03:32] And this is the expression as a function of the volume velocity.  
[03:35] As a function of the acceleration, it looks like this.  
[03:38] I'll remove the Y omega here.  
[03:41] So what this means is that the pressure at a distance is proportional to the acceleration of the diaphragm.  
[03:48] What this means is that the acceleration, the pressure, depends on the displacement through a factor of omega squared,  
[03:59] which means that we need larger displacements to get the same pressure at low frequencies.  
[04:04] Another characteristic is the so-called sensitivity in this case,  
[04:09] it's the pressure at a distance, a normalized distance, normalized voltage,  
[04:14] and this pressure is controlled by the mass.  
[04:17] Moving coil loudspeakers are high-pass filters, so this is different from dynamic microphones.  
[04:23] Now if we analyze the circuit, let's take the acoustical circuit, this is a very simple one.  
[04:30] we consider this when mounted on a buffer we have the same mass because we consider low frequency  
[04:37] and for the radiation impedance is just a mass ma1 we consider we have two masses one in the front  
[04:43] and one in the back this is the two ma1 here then in the mechanical circuit we have a mechanical  
[04:50] impedance which is all the elements of the diaphragm and suspension we call it ZM mechanical  
[04:56] impedance. And then in the electrical loop here we have the resistances and the impedance of the  
[05:04] coil with resistance included. If we combine all these expressions we get a volume-velocity  
[05:12] response, volume-velocity of the diaphragm, which is this function. In this we have assumed that the  
[05:19] Rg of the generator and the coil has no inductance, in order to simplify this.  
[05:28] This is an okay assumption for low frequencies. So if we take this  
[05:34] expression and we rewrite it a bit, we can make it as a function of the  
[05:42] parameters Mms, the total mass, and Rmd, which is the total resistance. Cms is only one  
[05:50] compliance, that's in this case mounting on a baffle, that's the suspension compliance.  
[05:58] A remark, mmd is the mass of the diaphragm and mms is the total mass, so remember the notation here.  
[06:08] And then again if we take this last expression of the volume velocity and we consider the expression  
[06:14] of the point source on a plane, then we can obtain after some rewriting here an expression for the  
[06:20] pressure and resistance as a function of the input voltage. So this is what we are after because this  
[06:29] is the performance of the loudspeaker, the pressure you get at some distance. This expression is  
[06:34] written as a function of the resonance frequency and the quality factor. Resonance frequency is a  
[06:40] function of the total mass and the compliance. Same for the quality factor with the addition  
[06:46] of the resistance totals. Again we take this pressure transfer function and then we can  
[06:54] observe that if we plot it for a generic case this is a high pass filter. We will be very interested  
[07:00] in this low frequency behavior that's why we have made an expression that is mostly  
[07:06] usable in low frequencies. We will mostly use all this analysis in low frequencies trying to get a  
[07:13] lowest cutoff frequency as low as possible trying to get a good behavior in this region  
[07:19] and then from this expression we can get a common parameter in the data sheets that's the sensitivity  
[07:27] of the loudspeaker and that's the constant time here so when this is one and that happens at  
[07:32] these frequencies when the response is constant this is the pressure at a distance it's usually  
[07:38] defined for a given voltage and a given distance it can be one volt voltage and one meter distance  
[07:45] as in this one but many data sheets they change these parameters you can have a voltage of 2.83  
[07:52] volts that corresponds to the one volt over eight ohms that's normalized and sometimes it's also  
[07:59] defined directly as one watt so this was one watt over eight volts or directly one watt because not  
[08:07] always we have eight volts as a DC resistance of the loudspeaker. It's also interesting looking at  
[08:18] the electrical input impedance of the loudspeaker because this is something that is accessible. We  
[08:24] are able to measure the electrical input impedance with some electrical equipment.  
[08:29] So if we develop that from the circuit we have these elements from the electrical part that  
[08:34] would be the resistance and the coil and this is called the emotional impedance. This contains the  
[08:40] mechanical and acoustic elements and it depends on the movement of the diaphragm. So it only exists  
[08:46] when the diaphragm is allowed to move. This is a standard version of it. This is how it looks like.  
[08:54] The coil and resistance make it so that the behavior is growing with frequency. That's what  
[09:04] a coil does. And then this peak here is the resonance represented by this term. From this  
[09:10] resonance, we can deduce parameters of the loudspeaker, as we will see later.  
[09:13] So, a loudspeaker is usually described by the so-called Thiele small parameters. Thiele and  
[09:22] more authors that first came up with this description. It's a set of parameters that  
[09:28] fully describes the unit. And these parameters are the resonance frequency, in this case angular  
[09:34] resonance frequency, and the Q factor, this is the total quality factor, that can be divided  
[09:44] into two specific quality factors, mechanical and electrical, that consider only mechanical  
[09:50] resistance and electrical resistance. Together they make up the total Q, but sometimes it's  
[09:55] interesting to look at those independently. And then the last still small parameter is called  
[10:02] equivalent volume. It's called equivalent volume because we make it as a volume, but in reality  
[10:07] this is just the compliance of the suspension, expressed as the volume that would have the same  
[10:12] compliance. It's a customary to do this. This is an example that you can try with some numeric  
[10:23] values. Here you have the solution of this example. It's just for showing how this is done. You can  
[10:29] calculate the total mass using these parameters, the resonance frequency using previous expressions,  
[10:35] the total resistance, and the QTS, the total quality factor from the previous data. Something  
[10:44] interesting to note is that when you mount the loudspeaker on a buffer, then you have  
[10:51] a radiation impedance in the front and a radiation impedance in the back. Either of them can be  
[10:56] represented on low frequencies like this. You can even remove this resistance and leave only the  
[11:02] mass. And this mass has this value only for one side, so in the end we have two of these masses,  
[11:08] one at the front and one at the back. When you mount the loudspeaker in FLIR, well, you don't  
[11:14] mounted, we just have it without any mounting. Then some calculations show that for low frequencies,  
[11:24] k8 less than 1 half, it can be represented by a similar circuit. In this case the mA1 has the  
[11:31] same value but it applies for both sides, meaning that as compared with this one, it's half the  
[11:36] value, it's half the mass, because this considers both sides. For both sides this would be 2 times mA1.  
[11:41] So it's not the same mounting the unit in free air or in a buffer. Another problem with this  
[11:50] kind of mounting is that, especially at low frequencies, these two polymerosities are  
[11:55] out of phase. They have opposite phase because the diaphragm moves like this,  
[11:59] so when it moves forward in this direction, it moves backwards in the other. So at low  
[12:03] frequencies there is what is called a short circuit between front and back and that hinders  
[12:08] the performance of the loudspeaker and the low frequencies. So, on it all what we have is that  
[12:15] when you don't mount the loudspeakers, you don't have any buffer, then you have a high  
[12:20] resonance frequency because of the lower mass. How do you calculate or measure those  
[12:28] still small parameters? So, you measure the input electrical impedance using a  
[12:35] circuit of this kind and the circuit consists on the loudspeaker that is  
[12:41] excited by a source and then in between we put a resistor. The function of the  
[12:46] resistor is sampling the electrical current through it. Its voltage  
[12:51] will be proportional to the current using Ohm's law. So if we measure this  
[12:55] voltage and this voltage then we can get voltage and current with the proper  
[12:59] operations and get impedance. However this in the practical sense that would be a ground here and we  
[13:07] cannot measure directly this voltage with equipment because it won't be grounded. So what we measure  
[13:12] is this voltage over the amplifier and the voltage on the unit and then by some operation we get this  
[13:18] voltage over the resistor and therefore the input impedance. So the first parameter we get here is  
[13:27] the resonance frequency, f0, thus the frequency at which we have the maximum. We can also easily get  
[13:32] the maximum impedance here, and we can also get the resistance at the C that you can also measure  
[13:39] with a ohmmeter, with a multimeter applied to the terminals without any excitation.  
[13:46] So, from the expression of the input electrical impedance you can get the value of the maximum  
[13:54] impedance. So the impedance at which you have this F1 and F2, which are half power bandwidth,  
[14:05] can be obtained like this, with Re and Z-marks, which are values that you have. So if you find  
[14:13] this impedance and find where they cut the curve, then you can get F1 and F2. And from F1 and F2,  
[14:20] and this value, then you can get the Q's, the total Q, electrical and, no, total Q here,  
[14:29] electrical and mechanical Q. So this accounts for all three small parameters except for one  
[14:36] that we have explained here. That's the next slide. The missing parameter is the compliance  
[14:44] of the suspension or equivalent volume. And there is a method to measure that where we have to  
[14:51] change something in the system in order to get the change in resonance frequency.  
[14:55] One thing you can change is the total mass. So if you add some extra mass to  
[15:01] the diaphragm, this is a kind of material, moldable material that is attached to  
[15:06] the diaphragm, that increases the mass and therefore the resonance frequency  
[15:10] changes. From this change in resonance frequency, you can deduce it, you can get  
[15:15] the parameters. So it's possible to get the parameters this way. MMS first and then from  
[15:22] that you can get all the parameters. Another way to do this, if you don't want to do this,  
[15:27] must change, is changing the other element here, that's the compliers. And the compliers you can  
[15:33] change by installing the unit on a close box where you know the volume, for example. This  
[15:39] This is actually what you would be doing in lab D.  
[15:42] At this point you solve problems 1 and 2 and we continue.  
[15:50] In the last part of the lecture we introduce a few interesting concepts.  
[15:58] The first one of them is the efficiency.  
[16:01] Any loudspeaker has efficiency that can be calculated as the ratio of acoustic power we get  
[16:09] over the electrical power we put into the loudspeaker.  
[16:14] The acoustic power we get through the radiation impedance and the volume velocity at mid  
[16:20] frequencies. This radiation impedance you can get from the circuit. You develop the circuit  
[16:28] into an expression and then they get the real part. This is what you get. And this is obtained  
[16:35] from the volume velocity response at mid frequencies. You can go back a few slides and  
[16:40] obtain this expression. The electrical power is a function of the current, or the voltage,  
[16:47] and the electrical resistance, the real power of the electrical resistance, which can be made Re.  
[16:55] With this, if you simplify it, you get this expression. And in this expression you can see  
[16:59] that you have more efficiency if you have a stronger magnetic field, or a longer coil,  
[17:04] or a larger surface, while a heavier diaphragm reduces the efficiency, as well as a larger  
[17:13] electrical resistance.  
[17:15] The values of efficiency in those speakers are very low, so usually below or around 1%.  
[17:22] It would be very difficult to get as high as 5%.  
[17:29] If you really want to increase the efficiency, you need to use other techniques like horns.  
[17:34] are not treated in this course, but they consist on having a form in front of the  
[17:40] loudspeaker that would adapt the impedance of the diaphragm to the environment around.  
[17:47] That has much more efficiency, but it has other problems of course.  
[17:51] So what this low efficiency means is that most of the electrical power is actually dissipated  
[17:56] as heat and that brings a problem because the coil heats up and this heat needs to be dissipated  
[18:04] somehow and that can create problems in some instances that can also alter the properties  
[18:10] of the loudspeaker it can function differently if it's hot so the thermal design is very important  
[18:20] another thing we are interested in is the displacement we can obtain an expression of  
[18:25] the displacement of the diaphragm as a function of time by integrating the velocity of the diaphragm  
[18:30] and the velocity you can obtain from the volume velocity in previous slides.  
[18:35] So you will end up with this expression that you can operate a bit to get this other expression  
[18:41] that is a function of the quality factor and the resonance frequency.  
[18:46] What we see in this expression, if you represent it as a function of frequency,  
[18:50] is that the displacement decreases with frequency as we anticipated earlier in this lecture.  
[18:57] So you need a lot of displacement and low frequencies to get the same pressure  
[19:02] at some distance. This you can also observe with the stroboscope demo that we have in the classroom.  
[19:09] If we continue with the diaphragm displacement, how is this dealt with in actual speakers?  
[19:22] The coil needs to move in order to create sound, so the coil will enter the region  
[19:29] you have a magnetic field and we don't want this coil to get out of the region or have a different  
[19:37] amount of coil inside the region so it's not a good idea to have the coil of the same height  
[19:43] as the gap where you have the magnetic field you either should have it longer than this height  
[19:50] or shorter this is what is called overhang coil and it will put more bounds of the coil  
[19:57] as they get out from this side and vice versa. This one works differently so this coil is not  
[20:05] supposed to get out of the region with magnetic field. This one is better for cooling but it's  
[20:13] less sensitive because you have more dead weight, this part of the coil is not producing any force  
[20:21] and you still have to have it. Whereas this has a coil that is bound over itself many times so  
[20:26] it's more difficult to cool down. These are the dimensions, the name of the dimensions of the gap  
[20:34] and the coil and if you want to calculate the maximum displacement you can get that from these  
[20:38] dimensions using these expressions which are the same with different sign for overhang or underhang  
[20:45] coils. One problem with excessive displacement is non-linearity. You can see that non-linearity  
[20:55] created by too much displacement has many effects. Your force factor will be different  
[21:02] as the coil moves around and outside the gap. The mechanical compliance will be different  
[21:07] because the suspension will move beyond its elasticity limit and won't behave the same.  
[21:14] It will be harder. The inductance will also be different as the coil moves away from the  
[21:21] magnetic field, so there's also undesirable effects. All these are undesirable effects.  
[21:26] Nonlinear effects manifest as the graded performance of the loudspeaker, distortion  
[21:34] on the output. So if, for example, we feed a sinusoidal signal into the loudspeaker,  
[21:39] we observe that not only the sinusoidal signal but also the harmonics of it will play in the  
[21:47] If we have a mix of sinusoidal signals, we can observe intermodulations.  
[21:51] This means that we have more sound that we fed into the loudspeaker in the first place.  
[21:56] All this field of nonlinearity in transducers is covered in the course Nonlinear Transducers in January.  
[22:03] Here we have some examples of distortion with different levels of input. We will play them from left to right.  
[22:11] Another effect that is very important in loudspeakers is what happens at high frequencies.  
[22:59] frequencies. So far we have been dealing with the low frequency part, low frequency circuit and so  
[23:05] on, but there is a limit to how high frequencies you can play with a given loudspeaker. This is  
[23:11] a plot from a datasheet, this is typical in datasheets, they plot the input impedance  
[23:18] and they also plot the response, pressure response for axial incidence and so on of  
[23:24] axis in certain angles. And what you can see here is that when you go high in frequencies there are  
[23:29] peaks and dips. These peaks and dips are due to what is called in loudspeaker jargon  
[23:35] break-up frequencies which are mechanical resonances in the diaphragm. The diaphragm  
[23:41] not anymore moves as one thing but it has movement inside. Here you can see another plot where  
[23:47] the diaphragm has been measured with a laser so we are seeing the voice call acceleration directly  
[23:53] not the pressure. You can see that at high frequencies this becomes very shaky. That's  
[23:58] because the diaphragm is not anymore a single diaphragm but it's radiating differently from  
[24:04] different regions of the diaphragm. With the specialized equipment like the Klipper system,  
[24:10] you can visualize those movements. It has a laser system that can scan the surface  
[24:18] and then exaggerate in those movements and you can see that there are modes on the diaphragm  
[24:22] that show at different frequencies. Of course you don't want to use the loudspeaker with this effect  
[24:31] so you try to cut down this with crossovers and combine with other units that have a higher  
[24:37] bandwidth. Yet another issue with loudspeakers is the losses in the inductance and the main  
[24:45] effect here is eddy currents. Eddy currents are currents that run within the polar pieces, the  
[24:50] metal parts that conduct the magnetic field in the gap. You can see this effect as having a voice  
[24:59] coil as a primary of a transformer. And then this transformer would have a secondary which is not  
[25:05] there, it's just shunted, short-circuited within the metal. That means there are currents running  
[25:14] inside the metal and heating it up. This heating of the metal is energy that is drawn from the  
[25:23] loss beaker and shows as losses. So the effect in the end is less inductance and increased losses.  
[25:31] So the inductor you have is an imperfect inductor. This is a video from a no longer existing company  
[25:41] I capture that shows currents in the metal parts as the coil moves up and down inside the gap.  
[25:51] The blocks here and other devices here are used in order to kind of homogenize this magnetic field  
[25:59] and make it more even and more linear. So how do you model this lossy inductance?  
[26:09] So one thing that is proposed is having this expression for the impedance of the inductor of the coil, having the L, the inductance, and then a G omega power something, less than 1, extra, and this will account for the losses.  
[26:28] This inductance, when you apply it to a current, I of D, then it shows as a partial derivative of the current.  
[26:38] In this plot you can see that the actual measurement is much closer to  
[26:42] this representation than the ideal inductor representation here.  
[26:48] So it works from a standard. You have to choose carefully the values of L and N.  
[26:53] How do you put this in a circuit, in an LTSpice circuit?  
[26:56] You can represent any impedance in LTSpice with a control source, a current source controlled by  
[27:04] voltage and you made it so that is its own voltage on the terminals of the source that controls it.  
[27:12] So we are relating with the control source voltage and current through the component. Therefore the  
[27:18] gain of the control source has to be the inverse of the impedance you want to represent in order  
[27:24] to fulfill Ohm's law, current equal voltage divided by impedance. So in this case if you  
[27:30] If you want to represent this inductance, then you have to write in the gain of the  
[27:36] control source this expression.  
[27:38] In LTSpice, when you write O equal, that means you have an expression of S, which  
[27:43] is a Laplace tensor function.  
[27:45] If you replace S by G , then you have this expression.  
[27:49] It has to be 1 over in order to fulfill the Ohm's law here.  
[27:53] This is how you fill it out in the properties of the source.  
[28:00] Finally, some considerations about near field and far field, this was part of lab A exercise,  
[28:06] remember the tube and the radiation from the tube, so a technique that is often used in order to  
[28:13] measure the output of a loudspeaker is measuring very close to the diaphragm. This is a near field  
[28:18] measurement in a circuit, in an analogy, that could be represented by the voltage or pressure  
[28:25] in the analogy, over the radiation impedance, so that the radiation impedance times volume  
[28:31] velocity of the diaphragm, and that's what we call in the circuit near-field pressure.  
[28:37] And the expression is like this, if you write MA1 here, this is the expression.  
[28:43] On the other hand, if you consider the volume velocity of the diaphragm, and then assume  
[28:48] this is a point source on a baffle, so you assume that the diaphragm is sitting on an  
[28:53] infinite buffer load in a box. Then the expression from point sources is like  
[28:58] this. Note that you have a 2 here, not a 4, because of the plane you have double  
[29:05] pressure, not the 4. So if you relate this near and far field pressures, they have  
[29:13] this expression. So there is a fixed number that relates near and far field  
[29:19] pressure. It's a function of the piston radius and the distance. So this means  
[29:25] that in principle a measurement in the near field can give you the response in the far field if you  
[29:30] use this expression. Of course measuring in the near field you would say that you only pick the  
[29:36] field from the loudspeaker but if you are in a normal room you will have room resonances and  
[29:40] that might show in the measurement. You will see this in lab D. And this is the end of the lecture  
[29:49] and this is the moment for the remaining exercises where you have a LTSpice simulation as well.  
[29:54] Thank you.  
