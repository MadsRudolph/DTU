---
course: "34870"
type: transcript
lecture: 8
source: "Slides/34870_Lecture_8_E26.mp4"
---
# Lecture 8 — transcript of the commented slides

> [!info] Machine transcript
> Whisper large-v3 (faster-whisper, GPU), English forced, vocabulary prompt. VCH speaks with a strong accent, so expect slips such as "buffer" = woofer, "pistol" = piston, "Tillis-Moll" = Thiele-Small. Timestamps are mm:ss into the video. The note: [[Lecture 8 - Loudspeaker Enclosures]].

[00:04] Welcome to the second lecture on loudspeakers in the electroacoustic traducers and systems course.  
[00:12] When a loudspeaker unit is played without any mounting, it experiences cancellation of  
[00:18] frequencies. The front and back radiations cancel out because they are out of phase.  
[00:22] We need to find another way of mounting them in order to get a better performance.  
[00:27] The first idea would be a buffer, as it was used in the previous lecture,  
[00:32] for the definition of the parameters. This is working but it's not very practical as it can be  
[00:38] very big and has to be big enough and it's bigger than the largest wavelength that happens at lower  
[00:46] frequency. Then another idea would be kind of folding the buffer and creating a box  
[00:54] that covers the back radiation. The back radiation of a unit would be in the box, it wouldn't  
[01:00] play outside the box in theory, so it wouldn't cancel with the front radiation. We'd only have  
[01:07] the front radiation of the unit. The issue is that the box loads the loudspeaker and limits  
[01:17] a bit the low frequency performance. So another option we have is using the back radiation by  
[01:26] placing a tube in the box. The tube together with the box create a hermoresonance, an additional  
[01:32] resonance that will help the radiation from the box together with the unit. In general what we  
[01:40] want from a box is to be small, not too big, and have a good low frequency response. All the  
[01:50] explanations in this lecture are aimed at low frequency response, so all circuits and  
[01:55] and derivations are made in the lowest frequency range. Therefore we have approximations in that sense.  
[02:05] So in any box design we have to find a compromise that  
[02:12] considers at the same time how much space we have, what is the price we want to pay  
[02:16] or give to our product, what performance we want and in all of this subjectivity is very important.  
[02:23] So we start with a closed box. A closed box can be sketched this way. We could have or not  
[02:33] dumping material inside the box and we draw this infinite baffle because we assume the unit is  
[02:40] radiating as if it was on an infinite baffle but the bag is contained in the box. We have three  
[02:49] new parameters to add to the circuit. One is the acoustic compliance of the bag volume. We have  
[02:55] some elasticity of the air here, so this is added to the mechanical compliance of the diaphragm.  
[03:02] Then we might have, if there is damping in the box, acoustic damping or resistance,  
[03:07] acoustic resistance. And then we have a mass load in the back. In the infinite  
[03:15] baffle we have the mass load corresponding to the radiation impedance. If the box is  
[03:21] big enough then this mass load is similar to the one corresponding to a buffer and very often we  
[03:27] will make this approximation. This MAV will be approximated as MA1 which is the one we have in  
[03:33] the front as well. The components can be represented in an impedance analogy like this  
[03:40] and then we call the box impedance set AB. How to calculate these parameters?  
[03:46] The acoustic compliance is simple enough if we have the volume of the box, effective volume of the box, that we call VAB, as you know from acoustic circuits.  
[03:59] However, if the box is filled with material, then this volume has to be reassessed because it's considered that the sound waves don't propagate with the same sound speed as in air with no filling.  
[04:12] filling. They are considered to be slower, so we assume that BAV would be slightly larger than the  
[04:19] physical volume, BV, of the box. And the amount of extra volume is difficult to estimate. The filling  
[04:30] is difficult to characterize, but usually it's 10-20% larger, depending. The second parameter  
[04:36] is the resistance, RAB. This must be estimated because it depends on the dumping material. So,  
[04:42] it can only be guessed. And then the acoustic mass with back volume. There are some empirical  
[04:48] formulas that you find in Leach for this that are related to the piston area of the diaphragm  
[04:58] and the surface of the face where the unit is mounted. There is an expression  
[05:05] with a b factor. This b factor enters into this formula where we know all the other  
[05:10] or the other quantities. You have several choices. You can say the D factor is 0.65,  
[05:18] which is the standard value. You can calculate it with this formula with the surfaces I mentioned,  
[05:22] or you could just say that it's equal to ma1. That's your choice depending on the situation.  
[05:29] This is the analogy, the circuit for this closed box. It's the same circuit as in the buffer with  
[05:39] the added components here. This is MAB, RAB, and CAB that are added to the back of the  
[05:46] diaphragm. In the baffle mounting we had another MA1 here. Now we have all these  
[05:52] three elements. And then the analysis is the same as in the baffle, so we don't  
[05:59] repeat the full analysis. We just take the volume-velocity response where we  
[06:05] have replaced the elements with elements that consider the new parts from the box,  
[06:13] but the expression is the same. The pressure response also follows the same expression.  
[06:18] And what do we have extra? It's this box component. The MMC, C goes for closed box,  
[06:24] has this new mass that sometimes can be assumed as the MA1, so in that case the total mass would  
[06:34] be the same as in the buffer. And then the total resistance as the extra time of REB and the total  
[06:40] compliance is not just the suspension compliance but it has added the compliance of the box. This  
[06:45] is an important issue here. A remark about a difference with leech when it has a different  
[06:54] definition of the resistance. So be careful when you use leech expressions in this.  
[06:58] So when you put all this together and do changes to get the quality factor and resonance frequency,  
[07:07] we get new expressions for resonance frequency of the closed-box system and Q-factor of the  
[07:13] closed-box system. They are not dependent on the total mass compliance and resistance which are  
[07:19] including these elements. This means that the resonance of the system in the closed-box is  
[07:25] different and usually higher than the one in a baffle. What is different?  
[07:33] What is different in a box compared with a baffle mounting? Well, first of all,  
[07:41] as I said before, you have an increased resonance frequency.  
[07:46] And if you make some approximations, like this mass approximation and so on, then we can  
[07:53] a person made the box resonance as the buffer mounted resonance times a factor square root  
[08:01] of 1 plus alpha. Alpha being the ratio of volumes. Volume of the box here and volume of the equivalent  
[08:11] volume of the suspension. This is the same as the ratio of compliances. If you remember the equivalent  
[08:19] volume of the suspension was related to the mechanical compliance of the suspension.  
[08:25] It's not a real volume, it's a mechanical elasticity when we express it as a volume.  
[08:32] This is the approximation we have made for this expression.  
[08:36] It's also possible to see what happens with the Q factor.  
[08:39] The Q factor is larger for a box as compared with a baffle mounting with the same factor.  
[08:47] In this case we have made the assumption that there is no feeling,  
[08:50] there is no resistance in order to arrive to this.  
[08:52] And then the effective volume of the box is increased because of the damping material.  
[09:01] I mentioned this before, but here you have the expression in Leech.  
[09:05] You might choose to use or not, it's a complicated expression.  
[09:08] It's okay to make approximations as long as you explain it and assume the errors.  
[09:16] And then the mechanical factor depends on the damping of the box, so this must be guessed  
[09:28] in the general case.  
[09:32] Usually there are some guess values, ranges, for unfilled and filled boxes that are used  
[09:38] for starting a design for a closed box.  
[09:42] These are the ranges you have.  
[09:46] Let's now do some considerations about the frequency response at low frequencies for  
[09:51] a closed box. These are the expressions from the previous slide on the resonance frequency of the  
[09:56] box, the ratio of volumes, alpha, and the quality factor. If we represent theoretical responses  
[10:06] for a given QTS and different volume ratios, alphas, then we can obtain different QTCs from  
[10:14] that. And we can observe here that we want to achieve the lowest catafrequency, which is the  
[10:21] catafrequency is the frequency at which you have a drop of 3 dB. We have to zoom in in this figure  
[10:28] to see what happens. There is one of the cores where you get the lowest 3 dB drop,  
[10:35] and that is corresponding to a QTC of 1 over square root of 2, approximately 0.71.  
[10:43] You can see here that this is the case here.  
[10:47] So this you can arrive to also mathematically.  
[10:51] This is the expression for the lowest cutoff frequency that you can get from the other  
[10:54] expressions by imposing this 3 dB drop.  
[10:58] So you see that for qtc, 1 over square root of 2, if you replace that here, all these  
[11:03] expressions cancel out, this becomes 1, and then fL, the cutoff frequency, is equal to  
[11:10] fg.  
[11:11] So very often you will be after this Qtc in your designs.  
[11:16] So if you are told in a problem that you want the lowest possible cutoff frequency, then  
[11:21] they are asking you to have a Qtc, a Q of the block system of 1 over square root of  
[11:28] 2.  
[11:31] In this slide we revisit the issue of efficiency.  
[11:33] If you remember from the mountain in a baffle, loudspeakers are not very efficient.  
[11:39] they have an efficiency of 1-2% if you are very likely close to 5%.  
[11:47] The expression we use here is the same that we did use for the waffle mounting, you just  
[11:51] replace the components that need to be replaced, MMC.  
[11:55] You can see or prove that you can derive this other expression for this one, which you can  
[12:02] do as an exercise yourself.  
[12:05] reason for driving this other expression is seeing the influence of different things.  
[12:10] And in this you can see that if you want to make the box small, you look at the total volume here,  
[12:16] which is the addition of the two volumes acoustically,  
[12:23] then you see that if you make the box small then it's less efficient. It's in the numerator.  
[12:28] In the numerator you also have a resonance frequency to the power of three. That means that  
[12:33] that lower resonant frequencies mean also lower efficiency.  
[12:41] So if you want a small box that has a good low frequency  
[12:44] performance, then it will be less efficient.  
[12:51] And these slides, we'll revisit.  
[12:53] This slide is from previous lecture.  
[12:54] That was the last one.  
[12:56] And this is about measuring the near or the far field.  
[12:59] We will recall this, and then we will  
[13:01] see how you implement this in LTSPICE.  
[13:04] Remember that the near field pressure  
[13:06] be calculated in the circuit as the volume velocity through the radiation impedance.  
[13:11] That would be current in the impedance analogy. This is the radiation impedance.  
[13:15] All low frequencies can be represented as a mass. So you get this. This is the expression  
[13:21] for the radiation impedance mass of a pistol and a rifle. In the far field, then you can  
[13:29] model the  
[13:33] loudspeaker as a point source on an infinite  
[13:37] plane, and as such you get this expression.  
[13:41] We use the volume velocity through the  
[13:45] radiation impedance and then project it to the far field using the point source  
[13:49] expression. The thing is that if you relate the two expressions  
[13:53] then you get an expression, a formula which is only dependent  
[13:57] on the distance and the piston radius. So there is a response at far field and a near field that  
[14:04] is the same but with different levels that allows measuring in the near field and getting far field  
[14:11] responses. So how do you get this in LTSpice? Repeat again, same concepts. This is a circuit  
[14:25] where we have created an external network here. It's a control source that just picks the voltage  
[14:32] or pressure in this analogy over the radiation impedance in the front and then divides by 20  
[14:38] micro which is the reference for SPL so that would be this figure here that's 1 over 20 micro  
[14:46] so when you click on this label and you will get a representation in dB which is SPL because we  
[14:52] assume that that all is excited by RMS values because SPL was with RMS but that's taken for  
[14:59] So, that would be the near field.  
[15:09] For the far field, we have another extra network, where you sample the volume velocity in this  
[15:15] case, not the voltage, but the current that is volume velocity in the radiation impedance.  
[15:23] And with that, and this expression, in this case the expression has a frequency dependence  
[15:27] or you have to use the feature of Laplace, if you write Laplace in this source here,  
[15:33] then you get a frequency dependence. This number is calculated as all these quantities here  
[15:41] that you need in order to have a level and a distance, a far field pressure level. So this  
[15:52] you can do in this device, with this device. And in this slide you have a kind of example  
[16:01] for designing a clock box. The most common requirements you get is, first case,  
[16:07] you want the lowest cutoff frequency, so you choose Qtc to be 1 over square root of 2,  
[16:14] as we said some slides ago, and then from the datasheet or measured parameters of the unit  
[16:20] on an infinite buffer, then we can reduce the box parameters. Since we have the Qtc,  
[16:26] we can get the alpha we are assuming on the approximations about mass, etc. So we get the  
[16:32] alpha, from that we can get the effective box volume. From the alpha we can also get the  
[16:39] threshold frequency of the box system and we can also get the cutoff frequency. That's one case.  
[16:47] Another possible case is you are given box volume, so you have the effective volume, from this you  
[16:54] have to the sine. So that means you readily have the alpha, the radius of volume, because you have  
[17:00] volume. From that you can get all the other parameters in a similar way. So this would be  
[17:05] two different kinds of the signs. In your case you might be given a unit, you might be asked to  
[17:12] choose a unit, so you will have to work your way through the equations depending on the case.  
[17:20] At this point we revisit the measurement of the Tillis-Moll parameters that we mentioned  
[17:25] in the previous lecture. In this case we will redo the calculation of the VAS, which is related to the  
[17:32] compliance of the suspension, by using this time a closed box. The idea is measuring without the  
[17:41] closed box, just a buffer, and measuring with the box, which means that we will have  
[17:48] the box parameters added. That means that instead of having the  
[17:51] the suspension compliance we have also the box compliance which can be calculated from  
[18:01] the volume of a box and this we can measure physically at this point it's very useful  
[18:08] to make the assumption that the mass at the back of the diaphragm is the same as the mass  
[18:14] at the front of the diaphragm which is the radiation impedance reduced to only a mass  
[18:19] This is not only convenient for the calculation but it's probably less subject to uncertainties  
[18:25] because if you don't do this you can still calculate VAS but it would be subject to the  
[18:31] uncertainties in other parameters that you need for this calculation. Then you can also obtain  
[18:39] alpha, the box ratio, from the relation of the frequency with closed box and with infinite buffer.  
[18:46] This can be possible because also the assumption we made here.  
[18:51] We also know that alpha is the ratio of box and suspension compliances.  
[18:58] From this and this, we can obtain Cs, the compliance of the suspension.  
[19:03] And from that, we can obtain, by multiplying by rho c squared, the Vs, the parameter we were looking for.  
[19:11] Use for solving problem one.  
[19:15] So, if we continue the lecture with the second setting, which is the vented box, this is  
[19:24] a somewhat more sophisticated, more complicated box design, where we use the radiation from  
[19:31] the back to help the performance of low frequencies.  
[19:34] Everything here deals with low frequencies.  
[19:36] Remember that we are concerned about low frequencies, so in a multiple unit box system, we will  
[19:42] only be doing this for the buffer unit.  
[19:47] So this can be seen as a second resonance that delays the back radiation and puts them  
[19:52] in phase with the front radiation.  
[19:57] So this is the circuit, the equivalence circuit of the box that has to be added to the equivalence  
[20:06] circuit of the unit, and in this case the total radiation perceived by a listener here  
[20:11] the summation of diaphragm resonance, bend, it's also called port, that's therefore the P,  
[20:18] or port volume velocity, and then we add a leakage, L leakage, the leaking,  
[20:26] volume velocity from the box. This leaking comes from any sound coming out from the box,  
[20:32] not through these two pads, that could be ceiling problems or radiation from vibration of a  
[20:40] plates forming the box, anything that leaks the sound inside to the outside. This leakage is very  
[20:45] important in vented boxes because it determines the Q factor of this resonance of the box-vent  
[20:53] system, which is a head-box resonance. So this is the given sequence where we have the mass of the  
[21:01] port or vent, that's the air included in this tube, the compliance of the box that we also had  
[21:08] before, and the leaking resistance. That's the resistance of sound coming out of a box.  
[21:14] It's really very high. So we need to sum these contributions. So it's not anymore as simple as  
[21:22] diaphragm volume velocity, but we have to deduce the U0, which is the sum of these three,  
[21:28] in this circuit. And we see here that the sum of these three can also be represented as minus  
[21:32] the volume velocity through the compliance of the box that we call U0.  
[21:43] So if we call this impedance ZA2, that will be the second acoustic impedance, or YA2 if  
[21:50] it's admittance, then that's found in the overall circuit for the vented box here in  
[21:58] this region.  
[21:59] The rest of the circuit is the same as in the buffer mounting.  
[22:05] that we have removed the coil inductance here and that's because we are only looking at very low  
[22:10] frequencies so the coil has little or very small impedance on that range so it's allowed for this  
[22:17] low frequency design to do that. So the transfer function is still the same we work with the same  
[22:24] original transfer function that we had for the baffle mounting but we add this extra term that  
[22:29] That would be the acoustic impedance for the vented box.  
[22:34] So, this is the elements in this tensor function.  
[22:42] So, in the case of the acoustical impedance, the mechanical one,  
[22:48] we assume for the analysis that Mab, as we have mentioned before in the closed box,  
[22:54] will be the same as Ma1. That means that the back mass of the unit  
[22:58] unit is the same as the front mass radiation impedance. It's a valid assumption for analysis  
[23:04] purposes. We also assume there is no filling, that there is no resistance due to the dumping material  
[23:11] in the box for analysis purposes. And then this part here is the impedance of the box system with  
[23:18] the tube with the resonance system. This is an extra resonance. So we have to find a means to  
[23:27] get this UCO, which is the total radiation. The UD is not enough because this is only the radiation  
[23:33] from the diaphragm. We need UCO. So we look at this circuit and then we find that the voltage  
[23:40] here, which is the pressure inside the box, can be expressed as the current through CAB times the  
[23:47] impedance of CAB, that would be this term here, but it can also be expressed as the voltage here,  
[23:52] which is the pressure in the box, through all the impedance Ca2. So this is this equivalence here.  
[24:00] So from this equivalence we can relate U0 and Ud that we have here as well.  
[24:05] From that we can get U0 as a function of Ud and find the expression for the total volume velocity  
[24:13] which is here. It's a function of this Ca1 and Ca2 etc. So from that we can get a full expression  
[24:21] of the pressure using the point-source  
[24:25] approximation, and it can be expressed this way  
[24:29] with some new parameters. The positional expression is more complicated  
[24:33] than in previous boxes or mountains.  
[24:37] It's a higher-order expression because we have two resonances.  
[24:41] So, here we have the expression again with the values  
[24:45] of the coefficients a1, a2, and a3.  
[24:48] And here, besides the alpha, radio of compliances or volumes, we have introduced a new parameter,  
[24:56] h, that's the radio of box resonance and mechanical resonance, h. We have these two  
[25:04] resonances here. These are the two resonances, driver resonance, mechanical resonance, and  
[25:10] bent box-head-both resonance, which is a function of the mass of the vent or port and the compliance  
[25:16] of the box. They both have their Q-factors, this you know, but this Q-factor of the  
[25:22] f-bar resonance depends on the leaking resistance you remember. That's why the leakage is important  
[25:27] because it determines the Q-factor of the box bent resonance. So how do you design a box like this?  
[25:37] It's a more involved design and there are countless possible designs. If you put together  
[25:44] a box without a proper design then you most probably would get a tuning or alignment,  
[25:50] that's how it's called. That is not one of the canonical ones because there are many ways of  
[25:56] doing this and high-end professional boxers use many tricks like signal processing or active  
[26:03] control or computers, anything. The classical canonical alignments are listed here in this table  
[26:11] And it can give you an idea of the possibilities of a work like this.  
[26:15] There is an alignment that is called for other Butterworth B4,  
[26:20] as this you can only achieve if your unit has a QTS of 0.4 exactly.  
[26:26] And in this case, all the expressions simplify totally and you get all the frequencies,  
[26:33] box resonance, mechanical resonance, lower cutoff, the same.  
[26:38] they are the same frequency. So this is a kind of lucky case where all the expressions simplify.  
[26:44] And then if your QTS is lower than this, then you will get an alignment that is called  
[26:50] QB3, where the cutoff frequency is larger than the unit on above and resonance.  
[27:00] Or if your QTS is higher than 0.4, then you get a lower  
[27:05] cut-off frequency than you had for the baffle mounting. These are the names of these alignments  
[27:13] Chebyshev, Kwasi-Waterworth. So with this one you get lower cut-off but you pay some price.  
[27:24] Note that if you just tune without following the design procedure you might get a tuning but it  
[27:33] might not be, most probably won't be a canonical tuning. It might be suboptimal or close to optimal  
[27:40] tuning. So this is a plot from Leech where you can see a box's design with canonical  
[27:52] settings or alignments. This would be the V4  
[27:56] alignment, the lucky one where you have all the frequencies the same for the Butterworth. If you  
[28:02] If you have quasi-water-bath, then you will get a higher cutoff.  
[28:08] If you have a Chebyshev alignment, then you get a lower cutoff, but you pay the price  
[28:14] of a ripple in the response, you will also have phase responses that will blur the response.  
[28:21] You get a lower cutoff, but at the price of less quality response, so what to choose depends  
[28:28] on the units available, the constraints in your design, and also how much distortion  
[28:37] and not optimal response are you willing to admit.  
[28:42] So there is no best tuning, it depends on many factors.  
[28:48] How do you design one of these alignments?  
[28:51] In leech you have plots like this.  
[28:53] There is one plot for every QL value.  
[28:56] QL depends on the leakage. If you remember, this is the Q factor of the box resonance, of the hermode resonance on the box unbent.  
[29:04] So if you choose one of these, for example QL7, which is this graphical design plot,  
[29:12] then you have to come up with a unit that has a given QTS. So this design is meant for starting with a given unit.  
[29:20] You find the value of QTS here, which would be somewhere between 0.4 and 0.5 in this case.  
[29:28] Then you draw a horizontal line and find the QTS curve here.  
[29:35] And then draw a vertical line and find where this vertical line cuts all the other curves and axes.  
[29:42] In this axis, you will find the alpha value corresponding to this QL and QTS.  
[29:48] And on the top ruler here, you will find what kind of alignment it is.  
[29:53] In this case, this is a Chebyshev alignment because it's on this region.  
[29:57] This would be a V4 alignment, and this would be a quasi-waterworth alignment.  
[30:01] So, and then when you cut these other curves, then you will get on this right-hand side  
[30:07] H and Q coefficients that will give you the lower cutoff and the box resonances, like this.  
[30:16] So with these two curves, as you can see here, if you had a unit of 0.4, then you would get  
[30:24] the same, all these two curves cross, and that means that H and Q are the same, and  
[30:29] FL and FB would be the same as predicted before. In this slide we have a kind of summary or  
[30:38] representation of what are the contributions of bend driver diaphragm and the total contribution  
[30:44] the sum of these two. As you can see there is a region of frequency where the bend radiation  
[30:49] dominates and then after that higher frequencies is the diaphragm or driver radiation that dominates.  
[30:58] So in a well-designed vented box system the two cooperate to get a total response that is optimal.  
[31:07] In this slide, I will represent the input electrical impedance of the pented box.  
[31:16] Remember that the input electrical impedance in the PATHEL unit was useful in order to get the  
[31:21] parameters of the unit. It is not so much so that you can get the parameters of the unit,  
[31:28] but you can get some information. As you can see here, if you have a  
[31:32] B4 for the Widerworth alignment, then the two peaks should have the same height here.  
[31:39] You get two peaks because there are two resonances there and this is a second order system. And then  
[31:46] this motion and impedance has two resonances. This is the electrical impedance which is the  
[31:52] same as above. These two peaks don't mean these are the two resonances, so not anymore as you  
[31:59] had in the Baffelt mounting, this is the resonance. This is not the fp and fs, this is different.  
[32:07] Actually, it is at the minimum between peaks that you have the box resonance.  
[32:13] And that's because you have a minimum of electrical impedance and a maximum of mechanical  
[32:17] impedance. Remember that the moving cold transduction inverses the impedance.  
[32:22] And actually you will see when you play in this box that at the box resonance, the driver finds  
[32:29] a lot of mechanical impedance and it will move less. So it is at this minimum electrical impedance  
[32:35] that you have the FB. Another remark here is that not always when you have these two equal  
[32:42] equal peaks you have a B4. You can have the two equal peaks and not being a B4. So if you get this  
[32:49] kind of response in your box and you haven't designed for a B4 then it's not a B4 most likely.  
[32:56] but for the V4 you have this property and equal peaks. If it's not a V4 you can  
[33:05] have either a situation where the first peak is lower than the second or you  
[33:13] could have the opposite. And finally on this design we are concerned about how  
[33:24] to design the port or vent. We just said it's a tube with a given mass but if you fix  
[33:31] mass of the part, then you still have freedom to choose the length and the surface or radius of the  
[33:38] tube. For a given mass, you can choose many pairs of length and surface. This expression,  
[33:49] if you remember from the initial lectures, is the physical length of the tube plus the end  
[33:54] end corrections. Remember that the end corrections replace the radiation impedance, so if you are to  
[34:02] include radiation impedance in a circuit, then you have to remove the corresponding part of the end  
[34:06] correction from the MAP. But going back to the issue of assigning the port, if you fix the  
[34:15] surface, if you take a given radius for the port, then you are defining also the length.  
[34:22] but a bit counterintuitive, the fact is that for a given mass, narrow tubes will be shorter than wider tubes,  
[34:33] so wider tubes will be longer for the same mass.  
[34:38] So if we want a wide tube, the problem could be that it won't fit in the box because it's longer.  
[34:44] But if we want a narrow tube, the problem could be that the flow of air through the tube can cause turbulence.  
[34:50] If you have been in the demo in the classroom, then you have noticed that there is a lot of flow, the air moves a lot in this tube.  
[34:58] So if the tube is narrow, then you will get turbulence and noise from turbulence.  
[35:02] That's why very often these tubes are rounded in the edges to prevent this kind of turbulence.  
[35:08] Then this slide is about another possibility you can have for boxes.  
[35:16] Instead of a vent, you can replace the vent by a passive radiator.  
[35:20] A passive radiator is just a unit that has no moving coil, it has no magnet, it just  
[35:27] has the diaphragm and the suspension.  
[35:30] So it's a mass on a spring and it acts very similarly to the vent, but instead of having  
[35:35] an acoustical mass, we have a mechanical mass.  
[35:38] This can be useful if you have problems of space in the design of your box, if you want  
[35:44] to make it very small, it's a more expensive solution, of course.  
[35:51] And this is the end of the lecture and this is time for solving the rest of the problems.  
