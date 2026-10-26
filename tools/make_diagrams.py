from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Rectangle
import numpy as np
A=Path(__file__).resolve().parent.parent/'assets'
INK='#173f35';GREEN='#397b61';GOLD='#b47e32';BG='#f4f8f5'
def canvas(title,w=10,h=5):
 fig,ax=plt.subplots(figsize=(w,h),dpi=160);fig.set_facecolor('white');ax.set(xlim=(0,10),ylim=(0,6));ax.axis('off');ax.set_title(title,fontweight='bold',color=INK,pad=14);return fig,ax
def box(ax,x,y,text,w=2,h=.8,critical=False):
 ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=.08',edgecolor=GOLD if critical else GREEN,facecolor='#fff3dc' if critical else BG,lw=2 if critical else 1));ax.text(x,y,text,ha='center',va='center',fontsize=10,color=INK)
def arrow(ax,p,q,label=None,rad=0,color=GREEN):
 ar=FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=14,lw=1.5,color=color,connectionstyle=f'arc3,rad={rad}');ax.add_patch(ar)
 if label:ax.text((p[0]+q[0])/2,(p[1]+q[1])/2+.15,label,ha='center',fontsize=9,color=INK)
def save(fig,name):fig.savefig(A/name,bbox_inches='tight',facecolor='white');plt.close(fig)
# Critical path: exact activity-on-node graph, top-down dependencies.
f,ax=canvas('2019–20 SPM · Critical path = 15 weeks',11,8)
pos={'A':(2,5.3),'B':(7.5,5.3),'C':(1,4.3),'D':(3,4.3),'E':(7.5,4.3),'F':(2,3.3),'G':(7.5,3.3),'J':(2,2.3),'H':(5.5,2.3),'I':(8.5,2.3),'K':(4,1.3),'L':(8.5,1.3),'M':(6.3,.3)}
d=dict(A=1,B=2,C=2,D=4,E=1,F=2,G=3,H=1,I=4,J=1,K=3,L=4,M=1);pred=dict(A=[],B=[],C=['A'],D=['A'],E=['B'],F=['C','D'],G=['E'],H=['G'],I=['G'],J=['F'],K=['J','H'],L=['I'],M=['K','L'])
cp=set(zip('BEGIL','EGILM'))
for child,parents in pred.items():
 for p in parents:arrow(ax,(pos[p][0],pos[p][1]-.27),(pos[child][0],pos[child][1]+.27),color=GOLD if (p,child) in cp else '#9eb5a8')
for k,(x,y) in pos.items():box(ax,x,y,f'{k} · {d[k]} w',1.2,.45,k in 'BEGILM')
save(f,'spm-critical-path.png')
# Risk choice branching, correct EV.
f,ax=canvas('Decision tree · Expected monetary value',10,4)
box(ax,1.3,3,'Choose',1.5)
box(ax,4.5,4.4,'Risky option\nEMV = 44,000',2.3,1)
box(ax,4.5,1.5,'Certain option\n35,000',2.3,1)
arrow(ax,(2.1,3.2),(3.2,4.2));arrow(ax,(2.1,2.7),(3.2,1.7))
box(ax,8.1,5,'+100,000',2,.7);box(ax,8.1,3.5,'−40,000',2,.7)
arrow(ax,(5.7,4.6),(7,5),'p = 0.6');arrow(ax,(5.7,4.1),(7,3.5),'p = 0.4')
save(f,'decision-risk.png')
# Loop diagrams with four nodes, feedback.
def cycle(name,title,labels):
 f,ax=canvas(title,9,5);pos=[(2.4,4.5),(7.4,4.5),(7.4,1.5),(2.4,1.5)]
 for (x,y),lab in zip(pos,labels):box(ax,x,y,lab,3.2,1.2)
 for p,q in [((4.1,4.5),(5.7,4.5)),((7.4,3.8),(7.4,2.2)),((5.7,1.5),(4.1,1.5)),((2.4,2.2),(2.4,3.8))]:arrow(ax,p,q)
 save(f,name)
cycle('spiral-cycle.png','Spiral model · repeated risk-driven cycles',['Objectives, alternatives\nand constraints','Analyze and resolve\nimportant risks','Develop and verify\nnext product increment','Review and plan\nthe next cycle'])
f,ax=canvas('Software project management · lifecycle and feedback',10,5)
for x,y,t in [(2,4.6,'Feasibility'),(7.5,4.6,'Planning'),(7.5,1.7,'Execute development\nand delivery'),(2,1.7,'Accept, hand over\nand close')]:box(ax,x,y,t,3,1)
arrow(ax,(3.6,4.6),(5.9,4.6));arrow(ax,(7.5,4),(7.5,2.3));arrow(ax,(5.9,1.7),(3.6,1.7));arrow(ax,(7.1,2.3),(7.1,4),label='Monitor / revise',rad=-.8)
save(f,'spm-lifecycle.png')
f,ax=canvas('k-means · assignment and update loop',9,5)
for x,y,t in [(2,4.5,'Choose k; initialize\ncentroids'),(7.4,4.5,'Assign each point to\nnearest centroid'),(7.4,1.5,'Update each centroid\nto cluster mean'),(2,1.5,'Converged or\niteration limit?')]:box(ax,x,y,t,3.2,1.1)
arrow(ax,(3.7,4.5),(5.7,4.5));arrow(ax,(7.4,3.9),(7.4,2.1));arrow(ax,(5.7,1.5),(3.7,1.5));arrow(ax,(2.4,2.1),(6.9,3.9),'No',rad=.2);ax.text(2,.3,'Yes → return clusters',ha='center',color=INK)
save(f,'kmeans-flow.png')
f,ax=canvas('Nested CV · one outer split (repeat over outer folds)',10,6)
box(ax,5,5.4,'Development data',4,.65)
box(ax,2.6,4,'Outer training folds',3.6,.7);box(ax,7.5,4,'Held-out outer test',3.6,.7)
arrow(ax,(4.4,5),(2.6,4.45));arrow(ax,(5.7,5),(7.5,4.45))
box(ax,2.6,2.6,'INNER CV\nCompare models + settings\nFit transforms inside folds',4,1.1);arrow(ax,(2.6,3.6),(2.6,3.2))
box(ax,2.6,1,'Select, then refit on\nall outer training data',4,.9);arrow(ax,(2.6,2),(2.6,1.5))
box(ax,7.5,1,'Score once on outer test\nAverage scores across splits',4,1);arrow(ax,(4.7,1),(5.4,1));arrow(ax,(7.5,3.6),(7.5,1.6))
save(f,'nested-cv.png')
f,axes=plt.subplots(1,3,figsize=(11,3.1),dpi=160)
for ax,rate,title in zip(axes,[.1,1,2.2],['Small η = 0.1','Suitable here: η = 1','Too large: η = 2.2']):
 w=4.;loss=[]
 for k in range(16):loss.append(.5*w*w);w=(1-rate)*w
 ax.plot(loss,color=GREEN,marker='o',markersize=3);ax.set_title(title);ax.set_xlabel('Update');ax.set_ylabel('Loss');ax.grid(alpha=.2)
f.suptitle('Exact example: J(w) = w²/2, starting w = 4',color=INK);f.tight_layout();save(f,'learning-rate.png')
# Memory diagram: no platform-specific offsets or live exploit instructions.
f,ax=canvas('Conceptual vulnerable stack frame · layout varies by platform',9,5)
for y,t in [(5,'Other frame data'),(3.8,'Saved control information'),(2.6,'Other local variables'),(1.4,'Fixed-size local buffer')]:box(ax,4.2,y,t,5.3,.85)
arrow(ax,(7.5,1.4),(7.5,4),'Unchecked write\nmay corrupt neighbors');ax.text(4.2,.2,'Bounds checks prevent writes beyond the allocated buffer.',ha='center',color=INK,fontsize=10)
save(f,'stack-overflow.png')
f,ax=canvas('Smurf · conceptual reflection / amplification',10,5)
box(ax,1.5,4.8,'Spoofed request\nsource = victim',2.6,1);box(ax,6.3,4.8,'Permissive\nbroadcast network',3,1);arrow(ax,(2.9,4.8),(4.7,4.8))
for x in [4.4,6.3,8.2]:
 box(ax,x,3,'Host',1.3,.7);arrow(ax,(6.3,4.2),(x,3.4));arrow(ax,(x,2.6),(6.3,1.3))
box(ax,6.3,.8,'Victim receives many replies',4.5,.7);save(f,'smurf-flow.png')
f,ax=canvas('Adware and spyware · distinct behaviors can overlap',10,4)
for y,t1,t2,t3 in [(4.5,'Advertising component','Select / fetch advertisement','Display advertisement'),(1.5,'Covert monitoring','Collect activity or data','Transmit without\nappropriate consent')]:
 for x,t in [(1.5,t1),(5,t2),(8.5,t3)]:box(ax,x,y,t,2.8,1.1)
 arrow(ax,(3, y),(3.5,y));arrow(ax,(6.5,y),(7,y))
ax.text(.1,5.6,'ADWARE',fontsize=10,color=GREEN);ax.text(.1,2.6,'SPYWARE',fontsize=10,color=GREEN);save(f,'adware-spyware.png')
f,ax=canvas('Conceptual TLS 1.3 handshake (ordinary full handshake)',10,6)
ax.text(2,5.8,'Client',ha='center',fontweight='bold');ax.text(8,5.8,'Server',ha='center',fontweight='bold')
ax.plot([2,2],[.4,5.5],color='#c4d6ca');ax.plot([8,8],[.4,5.5],color='#c4d6ca')
for y,p,q,lab in [(5.1,2,8,'ClientHello + key share'),(4.1,8,2,'ServerHello + key share'),(3,8,2,'Encrypted handshake: certificate, proof, Finished'),(1.8,2,8,'Client verifies identity; sends Finished')]:arrow(ax,(p,y),(q,y),lab)
arrow(ax,(2,.7),(8,.7),'Authenticated encrypted application data');save(f,'tls-flow.png')
f,ax=canvas('DNSSEC · chain of trust and validation',10,6)
for x,y,t in [(2.2,5,'Configured root trust anchor'),(2.2,3.4,'Parent DS → child DNSKEY'),(2.2,1.8,'Zone key verifies\nRRset signature (RRSIG)'),(7.5,3.4,'Validating resolver'),(7.5,1.1,'Valid: accept/cache\nBogus: reject')]:box(ax,x,y,t,3.9,.9)
arrow(ax,(2.2,4.5),(2.2,3.9));arrow(ax,(2.2,2.9),(2.2,2.3));arrow(ax,(4.25,1.9),(5.45,3.2),'Evidence');arrow(ax,(7.5,2.9),(7.5,1.7));save(f,'dnssec-flow.png')
print('Created 13 explanatory diagrams')
