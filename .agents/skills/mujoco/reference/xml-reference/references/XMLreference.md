# XML Reference

## Introduction

This chapter is the reference manual for the MJCF modeling language used in MuJoCo.

### XML schema

The dropdown below summarizes the XML elements and their attributes in MJCF. All information in MJCF is entered through elements and attributes. Text content in elements is not used (except for CDATA in [custom text](XMLreference.md) elements); if present, the parser ignores it.


html

The icons to the right of each element name have the following meaning:

|  |  |
|----|----|
| `star` | required element, can appear only once |
| `sync` | optional element, can appear multiple times recursively |
| `dot` | optional element, can appear only once |
| ​ | optional element, can appear multiple times (default case, no icon) |

<br/>


  <button onclick="document.querySelectorAll('.schema-small details').forEach(d => d.open = true)" class="sd-btn sd-btn-outline-primary sd-btn-sm">Expand All</button>
  <button onclick="document.querySelectorAll('.schema-small details details').forEach(d => d.open = false)" class="sd-btn sd-btn-outline-secondary sd-btn-sm" style="margin-left: 0.5em;">Collapse All</button>


`mujoco<mujoco>` `star`


2 3 4 4


`model<mujoco-model>`




`option<option>` ​


2 3 4 4


`timestep<option-timestep>`



`impratio<option-impratio>`



`tolerance<option-tolerance>`



`ls_tolerance<option-ls_tolerance>`



`noslip_tolerance<option-noslip_tolerance>`



`ccd_tolerance<option-ccd_tolerance>`



`sleep_tolerance<option-sleep_tolerance>`



`gravity<option-gravity>`



`wind<option-wind>`



`magnetic<option-magnetic>`



`density<option-density>`



`viscosity<option-viscosity>`



`o_margin<option-o_margin>`



`o_solref<option-o_solref>`



`o_solimp<option-o_solimp>`



`o_friction<option-o_friction>`



`integrator<option-integrator>`



`cone<option-cone>`



`jacobian<option-jacobian>`



`solver<option-solver>`



`iterations<option-iterations>`



`ls_iterations<option-ls_iterations>`



`noslip_iterations<option-noslip_iterations>`



`ccd_iterations<option-ccd_iterations>`



`sdf_iterations<option-sdf_iterations>`



`sdf_initpoints<option-sdf_initpoints>`



`actuatorgroupdisable<option-actuatorgroupdisable>`




`flag<option-flag>` `dot`


2 3 4 4


`constraint<option-flag-constraint>`



`equality<option-flag-equality>`



`frictionloss<option-flag-frictionloss>`



`limit<option-flag-limit>`



`contact<option-flag-contact>`



`spring<option-flag-spring>`



`damper<option-flag-damper>`



`gravity<option-flag-gravity>`



`clampctrl<option-flag-clampctrl>`



`warmstart<option-flag-warmstart>`



`filterparent<option-flag-filterparent>`



`actuation<option-flag-actuation>`



`refsafe<option-flag-refsafe>`



`sensor<option-flag-sensor>`



`midphase<option-flag-midphase>`



`eulerdamp<option-flag-eulerdamp>`



`autoreset<option-flag-autoreset>`



`nativeccd<option-flag-nativeccd>`



`island<option-flag-island>`



`multiccd<option-flag-multiccd>`



`override<option-flag-override>`



`energy<option-flag-energy>`



`fwdinv<option-flag-fwdinv>`



`invdiscrete<option-flag-invdiscrete>`



`sleep<option-flag-sleep>`



`diagexact<option-flag-diagexact>`



`ipc<option-flag-ipc>`



`speculative<option-flag-speculative>`






`compiler<compiler>` ​


2 3 4 4


`autolimits<compiler-autolimits>`



`boundmass<compiler-boundmass>`



`boundinertia<compiler-boundinertia>`



`settotalmass<compiler-settotalmass>`



`balanceinertia<compiler-balanceinertia>`



`strippath<compiler-strippath>`



`coordinate<compiler-coordinate>`



`angle<compiler-angle>`



`fitaabb<compiler-fitaabb>`



`eulerseq<compiler-eulerseq>`



`meshdir<compiler-meshdir>`



`texturedir<compiler-texturedir>`



`discardvisual<compiler-discardvisual>`



`usethread<compiler-usethread>`



`fusestatic<compiler-fusestatic>`



`inertiafromgeom<compiler-inertiafromgeom>`



`inertiagrouprange<compiler-inertiagrouprange>`



`saveinertial<compiler-saveinertial>`



`savecompiled<compiler-savecompiled>`



`savecanonical<compiler-savecanonical>`



`assetdir<compiler-assetdir>`



`alignfree<compiler-alignfree>`



`conflict<compiler-conflict>`



`passthrough<compiler-passthrough>`




`lengthrange<compiler-lengthrange>` `dot`


2 3 4 4


`mode<compiler-lengthrange-mode>`



`useexisting<compiler-lengthrange-useexisting>`



`uselimit<compiler-lengthrange-uselimit>`



`accel<compiler-lengthrange-accel>`



`maxforce<compiler-lengthrange-maxforce>`



`timeconst<compiler-lengthrange-timeconst>`



`timestep<compiler-lengthrange-timestep>`



`inttotal<compiler-lengthrange-inttotal>`



`interval<compiler-lengthrange-interval>`



`tolrange<compiler-lengthrange-tolrange>`






`size<size>` ​


2 3 4 4


`memory<size-memory>`



`njmax<size-njmax>`



`nconmax<size-nconmax>`



`nstack<size-nstack>`



`nuserdata<size-nuserdata>`



`nkey<size-nkey>`



`nuser_body<size-nuser_body>`



`nuser_jnt<size-nuser_jnt>`



`nuser_geom<size-nuser_geom>`



`nuser_site<size-nuser_site>`



`nuser_cam<size-nuser_cam>`



`nuser_tendon<size-nuser_tendon>`



`nuser_actuator<size-nuser_actuator>`



`nuser_sensor<size-nuser_sensor>`





`statistic<statistic>` ​


2 3 4 4


`meaninertia<statistic-meaninertia>`



`meanmass<statistic-meanmass>`



`meansize<statistic-meansize>`



`extent<statistic-extent>`



`center<statistic-center>`





`asset<asset>` ​


`mesh<asset-mesh>` ​


2 3 4 4


`name<asset-mesh-name>`



`class<asset-mesh-class>`



`content_type<asset-mesh-content_type>`



`file<asset-mesh-file>`



`vertex<asset-mesh-vertex>`



`normal<asset-mesh-normal>`



`texcoord<asset-mesh-texcoord>`



`face<asset-mesh-face>`



`refpos<asset-mesh-refpos>`



`refquat<asset-mesh-refquat>`



`scale<asset-mesh-scale>`



`smoothnormal<asset-mesh-smoothnormal>`



`maxhullvert<asset-mesh-maxhullvert>`



`inertia<asset-mesh-inertia>`



`builtin<asset-mesh-builtin>`



`params<asset-mesh-params>`



`material<asset-mesh-material>`




`plugin<mesh-plugin>` ​


2 3 4 4


`plugin<mesh-plugin-plugin>`



`instance<mesh-plugin-instance>`




`config<plugin-config>` ​


2 3 4 4


`key<plugin-config-key>`



`value<plugin-config-value>`







`hfield<asset-hfield>` ​


2 3 4 4


`name<asset-hfield-name>`



`content_type<asset-hfield-content_type>`



`file<asset-hfield-file>`



`nrow<asset-hfield-nrow>`



`ncol<asset-hfield-ncol>`



`size<asset-hfield-size>`



`elevation<asset-hfield-elevation>`





`skin<asset-skin>` ​


2 3 4 4


`name<asset-skin-name>`



`file<asset-skin-file>`



`material<asset-skin-material>`



`rgba<asset-skin-rgba>`



`inflate<asset-skin-inflate>`



`vertex<asset-skin-vertex>`



`texcoord<asset-skin-texcoord>`



`face<asset-skin-face>`



`group<asset-skin-group>`




`bone<skin-bone>` ​


2 3 4 4


`body<skin-bone-body>`



`bindpos<skin-bone-bindpos>`



`bindquat<skin-bone-bindquat>`



`vertid<skin-bone-vertid>`



`vertweight<skin-bone-vertweight>`






`texture<asset-texture>` ​


2 3 4 4


`name<asset-texture-name>`



`class<asset-texture-class>`



`type<asset-texture-type>`



`colorspace<asset-texture-colorspace>`



`content_type<asset-texture-content_type>`



`file<asset-texture-file>`



`gridsize<asset-texture-gridsize>`



`gridlayout<asset-texture-gridlayout>`



`fileright<asset-texture-fileright>`



`fileleft<asset-texture-fileleft>`



`fileup<asset-texture-fileup>`



`filedown<asset-texture-filedown>`



`filefront<asset-texture-filefront>`



`fileback<asset-texture-fileback>`



`builtin<asset-texture-builtin>`



`rgb1<asset-texture-rgb1>`



`rgb2<asset-texture-rgb2>`



`mark<asset-texture-mark>`



`markrgb<asset-texture-markrgb>`



`random<asset-texture-random>`



`width<asset-texture-width>`



`height<asset-texture-height>`



`hflip<asset-texture-hflip>`



`vflip<asset-texture-vflip>`



`nchannel<asset-texture-nchannel>`



`embed<asset-texture-embed>`





`material<asset-material>` ​


2 3 4 4


`name<asset-material-name>`



`class<asset-material-class>`



`texture<asset-material-texture>`



`texrepeat<asset-material-texrepeat>`



`texuniform<asset-material-texuniform>`



`emission<asset-material-emission>`



`specular<asset-material-specular>`



`shininess<asset-material-shininess>`



`reflectance<asset-material-reflectance>`



`metallic<asset-material-metallic>`



`roughness<asset-material-roughness>`



`rgba<asset-material-rgba>`




`layer<material-layer>` ​


2 3 4 4


`texture<material-layer-texture>`



`role<material-layer-role>`






`model<asset-model>` ​


2 3 4 4


`name<asset-model-name>`



`file<asset-model-file>`



`content_type<asset-model-content_type>`






`(world)body<body>` `sync`


2 3 4 4


`name<body-name>`



`childclass<body-childclass>`



`pos<body-pos>`



`quat<body-quat>`



`axisangle<body-axisangle>`



`xyaxes<body-xyaxes>`



`zaxis<body-zaxis>`



`euler<body-euler>`



`mocap<body-mocap>`



`gravcomp<body-gravcomp>`



`sleep<body-sleep>`



`simple<body-simple>`



`fuse<body-fuse>`



`user<body-user>`




`inertial<body-inertial>` `dot`


2 3 4 4


`pos<body-inertial-pos>`



`quat<body-inertial-quat>`



`mass<body-inertial-mass>`



`diaginertia<body-inertial-diaginertia>`



`axisangle<body-inertial-axisangle>`



`xyaxes<body-inertial-xyaxes>`



`zaxis<body-inertial-zaxis>`



`euler<body-inertial-euler>`



`fullinertia<body-inertial-fullinertia>`





`joint<body-joint>` ​


2 3 4 4


`name<body-joint-name>`



`class<body-joint-class>`



`type<body-joint-type>`



`group<body-joint-group>`



`pos<body-joint-pos>`



`axis<body-joint-axis>`



`springdamper<body-joint-springdamper>`



`limited<body-joint-limited>`



`actuatorfrclimited<body-joint-actuatorfrclimited>`



`solreflimit<body-joint-solreflimit>`



`solimplimit<body-joint-solimplimit>`



`solreffriction<body-joint-solreffriction>`



`solimpfriction<body-joint-solimpfriction>`



`stiffness<body-joint-stiffness>`



`range<body-joint-range>`



`actuatorfrcrange<body-joint-actuatorfrcrange>`



`actuatorgravcomp<body-joint-actuatorgravcomp>`



`margin<body-joint-margin>`



`ref<body-joint-ref>`



`springref<body-joint-springref>`



`springyield<body-joint-springyield>`



`armature<body-joint-armature>`



`damping<body-joint-damping>`



`frictionloss<body-joint-frictionloss>`



`user<body-joint-user>`





`freejoint<body-freejoint>` ​


2 3 4 4


`name<body-freejoint-name>`



`group<body-freejoint-group>`



`align<body-freejoint-align>`





`geom<body-geom>` ​


2 3 4 4


`name<body-geom-name>`



`class<body-geom-class>`



`type<body-geom-type>`



`contype<body-geom-contype>`



`conaffinity<body-geom-conaffinity>`



`condim<body-geom-condim>`



`group<body-geom-group>`



`priority<body-geom-priority>`



`size<body-geom-size>`



`material<body-geom-material>`



`friction<body-geom-friction>`



`mass<body-geom-mass>`



`density<body-geom-density>`



`shellinertia<body-geom-shellinertia>`



`solmix<body-geom-solmix>`



`solref<body-geom-solref>`



`solimp<body-geom-solimp>`



`margin<body-geom-margin>`



`gap<body-geom-gap>`



`surfacevel<body-geom-surfacevel>`



`adhesion<body-geom-adhesion>`



`fromto<body-geom-fromto>`



`pos<body-geom-pos>`



`quat<body-geom-quat>`



`axisangle<body-geom-axisangle>`



`xyaxes<body-geom-xyaxes>`



`zaxis<body-geom-zaxis>`



`euler<body-geom-euler>`



`hfield<body-geom-hfield>`



`mesh<body-geom-mesh>`



`fitscale<body-geom-fitscale>`



`rgba<body-geom-rgba>`



`castshadow<body-geom-castshadow>`



`fluidshape<body-geom-fluidshape>`



`fluidcoef<body-geom-fluidcoef>`



`user<body-geom-user>`




`plugin<geom-plugin>` ​


2 3 4 4


`plugin<geom-plugin-plugin>`



`instance<geom-plugin-instance>`




`config<plugin-config>` ​


2 3 4 4


`key<plugin-config-key>`



`value<plugin-config-value>`







`attach<body-attach>` ​


2 3 4 4


`model<body-attach-model>`



`body<body-attach-body>`



`frame<body-attach-frame>`



`prefix<body-attach-prefix>`





`site<body-site>` ​


2 3 4 4


`name<body-site-name>`



`class<body-site-class>`



`type<body-site-type>`



`group<body-site-group>`



`pos<body-site-pos>`



`quat<body-site-quat>`



`axisangle<body-site-axisangle>`



`xyaxes<body-site-xyaxes>`



`zaxis<body-site-zaxis>`



`euler<body-site-euler>`



`material<body-site-material>`



`mesh<body-site-mesh>`



`size<body-site-size>`



`fromto<body-site-fromto>`



`rgba<body-site-rgba>`



`user<body-site-user>`





`camera<body-camera>` ​


2 3 4 4


`name<body-camera-name>`



`class<body-camera-class>`



`projection<body-camera-projection>`



`fovy<body-camera-fovy>`



`ipd<body-camera-ipd>`



`resolution<body-camera-resolution>`



`output<body-camera-output>`



`pos<body-camera-pos>`



`quat<body-camera-quat>`



`axisangle<body-camera-axisangle>`



`xyaxes<body-camera-xyaxes>`



`zaxis<body-camera-zaxis>`



`euler<body-camera-euler>`



`mode<body-camera-mode>`



`target<body-camera-target>`



`focal<body-camera-focal>`



`focalpixel<body-camera-focalpixel>`



`principal<body-camera-principal>`



`principalpixel<body-camera-principalpixel>`



`sensorsize<body-camera-sensorsize>`



`user<body-camera-user>`





`light<body-light>` ​


2 3 4 4


`name<body-light-name>`



`class<body-light-class>`



`directional<body-light-directional>`



`type<body-light-type>`



`castshadow<body-light-castshadow>`



`active<body-light-active>`



`pos<body-light-pos>`



`dir<body-light-dir>`



`bulbradius<body-light-bulbradius>`



`intensity<body-light-intensity>`



`range<body-light-range>`



`attenuation<body-light-attenuation>`



`cutoff<body-light-cutoff>`



`softness<body-light-softness>`



`exponent<body-light-exponent>`



`ambient<body-light-ambient>`



`diffuse<body-light-diffuse>`



`specular<body-light-specular>`



`mode<body-light-mode>`



`target<body-light-target>`



`texture<body-light-texture>`





`plugin<body-plugin>` ​


2 3 4 4


`plugin<body-plugin-plugin>`



`instance<body-plugin-instance>`




`config<plugin-config>` ​


2 3 4 4


`key<plugin-config-key>`



`value<plugin-config-value>`






`flexcomp<body-flexcomp>` ​


2 3 4 4


`name<body-flexcomp-name>`



`type<body-flexcomp-type>`



`group<body-flexcomp-group>`



`dim<body-flexcomp-dim>`



`dof<body-flexcomp-dof>`



`count<body-flexcomp-count>`



`cellcount<body-flexcomp-cellcount>`



`spacing<body-flexcomp-spacing>`



`radius<body-flexcomp-radius>`



`rigid<body-flexcomp-rigid>`



`mass<body-flexcomp-mass>`



`inertiabox<body-flexcomp-inertiabox>`



`scale<body-flexcomp-scale>`



`file<body-flexcomp-file>`



`mesh<body-flexcomp-mesh>`



`point<body-flexcomp-point>`



`element<body-flexcomp-element>`



`texcoord<body-flexcomp-texcoord>`



`material<body-flexcomp-material>`



`rgba<body-flexcomp-rgba>`



`flatskin<body-flexcomp-flatskin>`



`pos<body-flexcomp-pos>`



`quat<body-flexcomp-quat>`



`axisangle<body-flexcomp-axisangle>`



`xyaxes<body-flexcomp-xyaxes>`



`zaxis<body-flexcomp-zaxis>`



`euler<body-flexcomp-euler>`



`origin<body-flexcomp-origin>`




`edge<flexcomp-edge>` `dot`


2 3 4 4


`equality<flexcomp-edge-equality>`



`solref<flexcomp-edge-solref>`



`solimp<flexcomp-edge-solimp>`



`stiffness<flexcomp-edge-stiffness>`



`damping<flexcomp-edge-damping>`





`elasticity<flexcomp-elasticity>` `dot`


2 3 4 4


`young<flexcomp-elasticity-young>`



`poisson<flexcomp-elasticity-poisson>`



`shear<flexcomp-elasticity-shear>`



`damping<flexcomp-elasticity-damping>`



`thickness<flexcomp-elasticity-thickness>`



`yield<flexcomp-elasticity-yield>`



`elastic2d<flexcomp-elasticity-elastic2d>`



`section<flexcomp-elasticity-section>`



`sectionsize<flexcomp-elasticity-sectionsize>`





`contact<flexcomp-contact>` `dot`


2 3 4 4


`contype<flexcomp-contact-contype>`



`conaffinity<flexcomp-contact-conaffinity>`



`condim<flexcomp-contact-condim>`



`priority<flexcomp-contact-priority>`



`friction<flexcomp-contact-friction>`



`solmix<flexcomp-contact-solmix>`



`solref<flexcomp-contact-solref>`



`solimp<flexcomp-contact-solimp>`



`margin<flexcomp-contact-margin>`



`gap<flexcomp-contact-gap>`



`selfcollide<flexcomp-contact-selfcollide>`



`activelayers<flexcomp-contact-activelayers>`



`passive<flexcomp-contact-passive>`





`pin<flexcomp-pin>` ​


2 3 4 4


`id<flexcomp-pin-id>`



`range<flexcomp-pin-range>`



`grid<flexcomp-pin-grid>`



`gridrange<flexcomp-pin-gridrange>`





`plugin<flexcomp-plugin>` ​


2 3 4 4


`plugin<flexcomp-plugin-plugin>`



`instance<flexcomp-plugin-instance>`




`config<plugin-config>` ​


2 3 4 4


`key<plugin-config-key>`



`value<plugin-config-value>`








`deformable<deformable>` ​


`flex<deformable-flex>` ​


2 3 4 4


`name<deformable-flex-name>`



`group<deformable-flex-group>`



`dim<deformable-flex-dim>`



`radius<deformable-flex-radius>`



`material<deformable-flex-material>`



`rgba<deformable-flex-rgba>`



`flatskin<deformable-flex-flatskin>`



`body<deformable-flex-body>`



`vertex<deformable-flex-vertex>`



`element<deformable-flex-element>`



`texcoord<deformable-flex-texcoord>`



`elemtexcoord<deformable-flex-elemtexcoord>`



`node<deformable-flex-node>`



`nodecoord<deformable-flex-nodecoord>`



`cellcount<deformable-flex-cellcount>`



`dof<deformable-flex-dof>`




`contact<flex-contact>` `dot`


2 3 4 4


`contype<flex-contact-contype>`



`conaffinity<flex-contact-conaffinity>`



`condim<flex-contact-condim>`



`priority<flex-contact-priority>`



`friction<flex-contact-friction>`



`solmix<flex-contact-solmix>`



`solref<flex-contact-solref>`



`solimp<flex-contact-solimp>`



`margin<flex-contact-margin>`



`gap<flex-contact-gap>`



`selfcollide<flex-contact-selfcollide>`



`activelayers<flex-contact-activelayers>`



`passive<flex-contact-passive>`





`edge<flex-edge>` `dot`


2 3 4 4


`stiffness<flex-edge-stiffness>`



`damping<flex-edge-damping>`





`elasticity<flex-elasticity>` `dot`


2 3 4 4


`young<flex-elasticity-young>`



`poisson<flex-elasticity-poisson>`



`shear<flex-elasticity-shear>`



`damping<flex-elasticity-damping>`



`thickness<flex-elasticity-thickness>`



`yield<flex-elasticity-yield>`



`elastic2d<flex-elasticity-elastic2d>`



`section<flex-elasticity-section>`



`sectionsize<flex-elasticity-sectionsize>`






`skin<deformable-skin>` ​


2 3 4 4


`name<deformable-skin-name>`



`file<deformable-skin-file>`



`material<deformable-skin-material>`



`rgba<deformable-skin-rgba>`



`inflate<deformable-skin-inflate>`



`vertex<deformable-skin-vertex>`



`texcoord<deformable-skin-texcoord>`



`face<deformable-skin-face>`



`group<deformable-skin-group>`




`bone<skin-bone>` ​


2 3 4 4


`body<skin-bone-body>`



`bindpos<skin-bone-bindpos>`



`bindquat<skin-bone-bindquat>`



`vertid<skin-bone-vertid>`



`vertweight<skin-bone-vertweight>`







`contact<contact>` ​


`pair<contact-pair>` ​


2 3 4 4


`name<contact-pair-name>`



`class<contact-pair-class>`



`geom1<contact-pair-geom1>`



`geom2<contact-pair-geom2>`



`condim<contact-pair-condim>`



`friction<contact-pair-friction>`



`solref<contact-pair-solref>`



`solreffriction<contact-pair-solreffriction>`



`solimp<contact-pair-solimp>`



`gap<contact-pair-gap>`



`margin<contact-pair-margin>`



`adhesion<contact-pair-adhesion>`





`exclude<contact-exclude>` ​


2 3 4 4


`name<contact-exclude-name>`



`body1<contact-exclude-body1>`



`body2<contact-exclude-body2>`






`equality<equality>` ​


`connect<equality-connect>` ​


2 3 4 4


`name<equality-connect-name>`



`class<equality-connect-class>`



`active<equality-connect-active>`



`solref<equality-connect-solref>`



`solimp<equality-connect-solimp>`



`body1<equality-connect-body1>`



`body2<equality-connect-body2>`



`anchor<equality-connect-anchor>`



`site1<equality-connect-site1>`



`site2<equality-connect-site2>`





`weld<equality-weld>` ​


2 3 4 4


`name<equality-weld-name>`



`class<equality-weld-class>`



`active<equality-weld-active>`



`solref<equality-weld-solref>`



`solimp<equality-weld-solimp>`



`body1<equality-weld-body1>`



`body2<equality-weld-body2>`



`relpose<equality-weld-relpose>`



`anchor<equality-weld-anchor>`



`site1<equality-weld-site1>`



`site2<equality-weld-site2>`



`torquescale<equality-weld-torquescale>`





`joint<equality-joint>` ​


2 3 4 4


`name<equality-joint-name>`



`class<equality-joint-class>`



`active<equality-joint-active>`



`solref<equality-joint-solref>`



`solimp<equality-joint-solimp>`



`joint1<equality-joint-joint1>`



`joint2<equality-joint-joint2>`



`polycoef<equality-joint-polycoef>`





`tendon<equality-tendon>` ​


2 3 4 4


`name<equality-tendon-name>`



`class<equality-tendon-class>`



`active<equality-tendon-active>`



`solref<equality-tendon-solref>`



`solimp<equality-tendon-solimp>`



`tendon1<equality-tendon-tendon1>`



`tendon2<equality-tendon-tendon2>`



`polycoef<equality-tendon-polycoef>`





`flex<equality-flex>` ​


2 3 4 4


`name<equality-flex-name>`



`class<equality-flex-class>`



`active<equality-flex-active>`



`solref<equality-flex-solref>`



`solimp<equality-flex-solimp>`



`flex<equality-flex-flex>`





`flexstrain<equality-flexstrain>` ​


2 3 4 4


`name<equality-flexstrain-name>`



`class<equality-flexstrain-class>`



`active<equality-flexstrain-active>`



`solref<equality-flexstrain-solref>`



`solimp<equality-flexstrain-solimp>`



`flex<equality-flexstrain-flex>`



`cell<equality-flexstrain-cell>`






`tendon<tendon>` ​


`spatial<tendon-spatial>` ​


2 3 4 4


`name<tendon-spatial-name>`



`class<tendon-spatial-class>`



`group<tendon-spatial-group>`



`limited<tendon-spatial-limited>`



`actuatorfrclimited<tendon-spatial-actuatorfrclimited>`



`range<tendon-spatial-range>`



`actuatorfrcrange<tendon-spatial-actuatorfrcrange>`



`solreflimit<tendon-spatial-solreflimit>`



`solimplimit<tendon-spatial-solimplimit>`



`solreffriction<tendon-spatial-solreffriction>`



`solimpfriction<tendon-spatial-solimpfriction>`



`frictionloss<tendon-spatial-frictionloss>`



`springlength<tendon-spatial-springlength>`



`springyield<tendon-spatial-springyield>`



`width<tendon-spatial-width>`



`material<tendon-spatial-material>`



`margin<tendon-spatial-margin>`



`stiffness<tendon-spatial-stiffness>`



`damping<tendon-spatial-damping>`



`armature<tendon-spatial-armature>`



`rgba<tendon-spatial-rgba>`



`user<tendon-spatial-user>`




`site<spatial-site>` ​


2 3 4 4


`site<spatial-site-site>`





`geom<spatial-geom>` ​


2 3 4 4


`geom<spatial-geom-geom>`



`sidesite<spatial-geom-sidesite>`





`pulley<spatial-pulley>` ​


2 3 4 4


`divisor<spatial-pulley-divisor>`






`fixed<tendon-fixed>` ​


2 3 4 4


`name<tendon-fixed-name>`



`class<tendon-fixed-class>`



`group<tendon-fixed-group>`



`limited<tendon-fixed-limited>`



`actuatorfrclimited<tendon-fixed-actuatorfrclimited>`



`range<tendon-fixed-range>`



`actuatorfrcrange<tendon-fixed-actuatorfrcrange>`



`solreflimit<tendon-fixed-solreflimit>`



`solimplimit<tendon-fixed-solimplimit>`



`solreffriction<tendon-fixed-solreffriction>`



`solimpfriction<tendon-fixed-solimpfriction>`



`frictionloss<tendon-fixed-frictionloss>`



`springlength<tendon-fixed-springlength>`



`springyield<tendon-fixed-springyield>`



`margin<tendon-fixed-margin>`



`stiffness<tendon-fixed-stiffness>`



`damping<tendon-fixed-damping>`



`armature<tendon-fixed-armature>`



`user<tendon-fixed-user>`




`joint<fixed-joint>` ​


2 3 4 4


`joint<fixed-joint-joint>`



`coef<fixed-joint-coef>`







`actuator<actuator>` ​


`general<actuator-general>` ​


2 3 4 4


`name<actuator-general-name>`



`class<actuator-general-class>`



`group<actuator-general-group>`



`nsample<actuator-general-nsample>`



`interp<actuator-general-interp>`



`delay<actuator-general-delay>`



`ctrlrange<actuator-general-ctrlrange>`



`user<actuator-general-user>`



`ctrllimited<actuator-general-ctrllimited>`



`forcelimited<actuator-general-forcelimited>`



`actlimited<actuator-general-actlimited>`



`forcerange<actuator-general-forcerange>`



`actrange<actuator-general-actrange>`



`lengthrange<actuator-general-lengthrange>`



`gear<actuator-general-gear>`



`damping<actuator-general-damping>`



`armature<actuator-general-armature>`



`cranklength<actuator-general-cranklength>`



`joint<actuator-general-joint>`



`jointinparent<actuator-general-jointinparent>`



`tendon<actuator-general-tendon>`



`slidersite<actuator-general-slidersite>`



`cranksite<actuator-general-cranksite>`



`site<actuator-general-site>`



`refsite<actuator-general-refsite>`



`body<actuator-general-body>`



`actdim<actuator-general-actdim>`



`input<actuator-general-input>`



`velrange<actuator-general-velrange>`



`ffrange<actuator-general-ffrange>`



`inheritrange<actuator-general-inheritrange>`



`dyntype<actuator-general-dyntype>`



`gaintype<actuator-general-gaintype>`



`biastype<actuator-general-biastype>`



`dynprm<actuator-general-dynprm>`



`gainprm<actuator-general-gainprm>`



`biasprm<actuator-general-biasprm>`



`actearly<actuator-general-actearly>`





`motor<actuator-motor>` ​


2 3 4 4


`name<actuator-motor-name>`



`class<actuator-motor-class>`



`group<actuator-motor-group>`



`nsample<actuator-motor-nsample>`



`interp<actuator-motor-interp>`



`delay<actuator-motor-delay>`



`ctrlrange<actuator-motor-ctrlrange>`



`user<actuator-motor-user>`



`ctrllimited<actuator-motor-ctrllimited>`



`forcelimited<actuator-motor-forcelimited>`



`forcerange<actuator-motor-forcerange>`



`lengthrange<actuator-motor-lengthrange>`



`gear<actuator-motor-gear>`



`damping<actuator-motor-damping>`



`armature<actuator-motor-armature>`



`cranklength<actuator-motor-cranklength>`



`joint<actuator-motor-joint>`



`jointinparent<actuator-motor-jointinparent>`



`tendon<actuator-motor-tendon>`



`slidersite<actuator-motor-slidersite>`



`cranksite<actuator-motor-cranksite>`



`site<actuator-motor-site>`



`refsite<actuator-motor-refsite>`





`position<actuator-position>` ​


2 3 4 4


`name<actuator-position-name>`



`class<actuator-position-class>`



`group<actuator-position-group>`



`nsample<actuator-position-nsample>`



`interp<actuator-position-interp>`



`delay<actuator-position-delay>`



`ctrlrange<actuator-position-ctrlrange>`



`user<actuator-position-user>`



`ctrllimited<actuator-position-ctrllimited>`



`forcelimited<actuator-position-forcelimited>`



`inheritrange<actuator-position-inheritrange>`



`forcerange<actuator-position-forcerange>`



`lengthrange<actuator-position-lengthrange>`



`gear<actuator-position-gear>`



`damping<actuator-position-damping>`



`armature<actuator-position-armature>`



`cranklength<actuator-position-cranklength>`



`joint<actuator-position-joint>`



`jointinparent<actuator-position-jointinparent>`



`tendon<actuator-position-tendon>`



`slidersite<actuator-position-slidersite>`



`cranksite<actuator-position-cranksite>`



`site<actuator-position-site>`



`refsite<actuator-position-refsite>`



`kp<actuator-position-kp>`



`kv<actuator-position-kv>`



`dampratio<actuator-position-dampratio>`



`timeconst<actuator-position-timeconst>`





`velocity<actuator-velocity>` ​


2 3 4 4


`name<actuator-velocity-name>`



`class<actuator-velocity-class>`



`group<actuator-velocity-group>`



`nsample<actuator-velocity-nsample>`



`interp<actuator-velocity-interp>`



`delay<actuator-velocity-delay>`



`ctrlrange<actuator-velocity-ctrlrange>`



`user<actuator-velocity-user>`



`ctrllimited<actuator-velocity-ctrllimited>`



`forcelimited<actuator-velocity-forcelimited>`



`forcerange<actuator-velocity-forcerange>`



`lengthrange<actuator-velocity-lengthrange>`



`gear<actuator-velocity-gear>`



`damping<actuator-velocity-damping>`



`armature<actuator-velocity-armature>`



`cranklength<actuator-velocity-cranklength>`



`joint<actuator-velocity-joint>`



`jointinparent<actuator-velocity-jointinparent>`



`tendon<actuator-velocity-tendon>`



`slidersite<actuator-velocity-slidersite>`



`cranksite<actuator-velocity-cranksite>`



`site<actuator-velocity-site>`



`refsite<actuator-velocity-refsite>`



`kv<actuator-velocity-kv>`





`intvelocity<actuator-intvelocity>` ​


2 3 4 4


`name<actuator-intvelocity-name>`



`class<actuator-intvelocity-class>`



`group<actuator-intvelocity-group>`



`nsample<actuator-intvelocity-nsample>`



`interp<actuator-intvelocity-interp>`



`delay<actuator-intvelocity-delay>`



`ctrlrange<actuator-intvelocity-ctrlrange>`



`user<actuator-intvelocity-user>`



`ctrllimited<actuator-intvelocity-ctrllimited>`



`forcelimited<actuator-intvelocity-forcelimited>`



`actlimited<actuator-intvelocity-actlimited>`



`forcerange<actuator-intvelocity-forcerange>`



`actrange<actuator-intvelocity-actrange>`



`inheritrange<actuator-intvelocity-inheritrange>`



`lengthrange<actuator-intvelocity-lengthrange>`



`gear<actuator-intvelocity-gear>`



`damping<actuator-intvelocity-damping>`



`armature<actuator-intvelocity-armature>`



`cranklength<actuator-intvelocity-cranklength>`



`joint<actuator-intvelocity-joint>`



`jointinparent<actuator-intvelocity-jointinparent>`



`tendon<actuator-intvelocity-tendon>`



`slidersite<actuator-intvelocity-slidersite>`



`cranksite<actuator-intvelocity-cranksite>`



`site<actuator-intvelocity-site>`



`refsite<actuator-intvelocity-refsite>`



`kp<actuator-intvelocity-kp>`



`kv<actuator-intvelocity-kv>`



`dampratio<actuator-intvelocity-dampratio>`





`orientation<actuator-orientation>` ​


2 3 4 4


`name<actuator-orientation-name>`



`class<actuator-orientation-class>`



`group<actuator-orientation-group>`



`nsample<actuator-orientation-nsample>`



`interp<actuator-orientation-interp>`



`delay<actuator-orientation-delay>`



`ctrlrange<actuator-orientation-ctrlrange>`



`user<actuator-orientation-user>`



`forcelimited<actuator-orientation-forcelimited>`



`forcerange<actuator-orientation-forcerange>`



`joint<actuator-orientation-joint>`



`site<actuator-orientation-site>`



`refsite<actuator-orientation-refsite>`



`kp<actuator-orientation-kp>`



`kv<actuator-orientation-kv>`



`dampratio<actuator-orientation-dampratio>`



`input<actuator-orientation-input>`





`pid<actuator-pid>` ​


2 3 4 4


`name<actuator-pid-name>`



`class<actuator-pid-class>`



`group<actuator-pid-group>`



`nsample<actuator-pid-nsample>`



`interp<actuator-pid-interp>`



`delay<actuator-pid-delay>`



`ctrlrange<actuator-pid-ctrlrange>`



`user<actuator-pid-user>`



`ctrllimited<actuator-pid-ctrllimited>`



`forcelimited<actuator-pid-forcelimited>`



`posrange<actuator-pid-posrange>`



`velrange<actuator-pid-velrange>`



`ffrange<actuator-pid-ffrange>`



`forcerange<actuator-pid-forcerange>`



`inheritrange<actuator-pid-inheritrange>`



`lengthrange<actuator-pid-lengthrange>`



`gear<actuator-pid-gear>`



`damping<actuator-pid-damping>`



`armature<actuator-pid-armature>`



`cranklength<actuator-pid-cranklength>`



`joint<actuator-pid-joint>`



`jointinparent<actuator-pid-jointinparent>`



`tendon<actuator-pid-tendon>`



`slidersite<actuator-pid-slidersite>`



`cranksite<actuator-pid-cranksite>`



`site<actuator-pid-site>`



`refsite<actuator-pid-refsite>`



`kp<actuator-pid-kp>`



`kv<actuator-pid-kv>`



`dampratio<actuator-pid-dampratio>`



`ki<actuator-pid-ki>`



`imax<actuator-pid-imax>`



`slewmax<actuator-pid-slewmax>`



`input<actuator-pid-input>`





`damper<actuator-damper>` ​


2 3 4 4


`name<actuator-damper-name>`



`class<actuator-damper-class>`



`group<actuator-damper-group>`



`nsample<actuator-damper-nsample>`



`interp<actuator-damper-interp>`



`delay<actuator-damper-delay>`



`ctrlrange<actuator-damper-ctrlrange>`



`user<actuator-damper-user>`



`forcelimited<actuator-damper-forcelimited>`



`forcerange<actuator-damper-forcerange>`



`lengthrange<actuator-damper-lengthrange>`



`gear<actuator-damper-gear>`



`damping<actuator-damper-damping>`



`armature<actuator-damper-armature>`



`cranklength<actuator-damper-cranklength>`



`joint<actuator-damper-joint>`



`jointinparent<actuator-damper-jointinparent>`



`tendon<actuator-damper-tendon>`



`slidersite<actuator-damper-slidersite>`



`cranksite<actuator-damper-cranksite>`



`site<actuator-damper-site>`



`refsite<actuator-damper-refsite>`



`kv<actuator-damper-kv>`





`cylinder<actuator-cylinder>` ​


2 3 4 4


`name<actuator-cylinder-name>`



`class<actuator-cylinder-class>`



`group<actuator-cylinder-group>`



`nsample<actuator-cylinder-nsample>`



`interp<actuator-cylinder-interp>`



`delay<actuator-cylinder-delay>`



`ctrlrange<actuator-cylinder-ctrlrange>`



`user<actuator-cylinder-user>`



`ctrllimited<actuator-cylinder-ctrllimited>`



`forcelimited<actuator-cylinder-forcelimited>`



`forcerange<actuator-cylinder-forcerange>`



`lengthrange<actuator-cylinder-lengthrange>`



`gear<actuator-cylinder-gear>`



`damping<actuator-cylinder-damping>`



`armature<actuator-cylinder-armature>`



`cranklength<actuator-cylinder-cranklength>`



`joint<actuator-cylinder-joint>`



`jointinparent<actuator-cylinder-jointinparent>`



`tendon<actuator-cylinder-tendon>`



`slidersite<actuator-cylinder-slidersite>`



`cranksite<actuator-cylinder-cranksite>`



`site<actuator-cylinder-site>`



`refsite<actuator-cylinder-refsite>`



`timeconst<actuator-cylinder-timeconst>`



`area<actuator-cylinder-area>`



`diameter<actuator-cylinder-diameter>`



`bias<actuator-cylinder-bias>`





`muscle<actuator-muscle>` ​


2 3 4 4


`name<actuator-muscle-name>`



`class<actuator-muscle-class>`



`group<actuator-muscle-group>`



`nsample<actuator-muscle-nsample>`



`interp<actuator-muscle-interp>`



`delay<actuator-muscle-delay>`



`ctrlrange<actuator-muscle-ctrlrange>`



`user<actuator-muscle-user>`



`ctrllimited<actuator-muscle-ctrllimited>`



`forcelimited<actuator-muscle-forcelimited>`



`forcerange<actuator-muscle-forcerange>`



`lengthrange<actuator-muscle-lengthrange>`



`gear<actuator-muscle-gear>`



`damping<actuator-muscle-damping>`



`armature<actuator-muscle-armature>`



`cranklength<actuator-muscle-cranklength>`



`joint<actuator-muscle-joint>`



`jointinparent<actuator-muscle-jointinparent>`



`tendon<actuator-muscle-tendon>`



`slidersite<actuator-muscle-slidersite>`



`cranksite<actuator-muscle-cranksite>`



`timeconst<actuator-muscle-timeconst>`



`tausmooth<actuator-muscle-tausmooth>`



`range<actuator-muscle-range>`



`force<actuator-muscle-force>`



`scale<actuator-muscle-scale>`



`lmin<actuator-muscle-lmin>`



`lmax<actuator-muscle-lmax>`



`vmax<actuator-muscle-vmax>`



`fpmax<actuator-muscle-fpmax>`



`fvmax<actuator-muscle-fvmax>`





`adhesion<actuator-adhesion>` ​


2 3 4 4


`name<actuator-adhesion-name>`



`class<actuator-adhesion-class>`



`group<actuator-adhesion-group>`



`nsample<actuator-adhesion-nsample>`



`interp<actuator-adhesion-interp>`



`delay<actuator-adhesion-delay>`



`ctrlrange<actuator-adhesion-ctrlrange>`



`user<actuator-adhesion-user>`



`forcelimited<actuator-adhesion-forcelimited>`



`forcerange<actuator-adhesion-forcerange>`



`body<actuator-adhesion-body>`



`gain<actuator-adhesion-gain>`





`dcmotor<actuator-dcmotor>` ​


2 3 4 4


`name<actuator-dcmotor-name>`



`class<actuator-dcmotor-class>`



`group<actuator-dcmotor-group>`



`nsample<actuator-dcmotor-nsample>`



`interp<actuator-dcmotor-interp>`



`delay<actuator-dcmotor-delay>`



`ctrlrange<actuator-dcmotor-ctrlrange>`



`user<actuator-dcmotor-user>`



`ctrllimited<actuator-dcmotor-ctrllimited>`



`lengthrange<actuator-dcmotor-lengthrange>`



`gear<actuator-dcmotor-gear>`



`damping<actuator-dcmotor-damping>`



`armature<actuator-dcmotor-armature>`



`cranklength<actuator-dcmotor-cranklength>`



`joint<actuator-dcmotor-joint>`



`jointinparent<actuator-dcmotor-jointinparent>`



`tendon<actuator-dcmotor-tendon>`



`slidersite<actuator-dcmotor-slidersite>`



`cranksite<actuator-dcmotor-cranksite>`



`site<actuator-dcmotor-site>`



`refsite<actuator-dcmotor-refsite>`



`motorconst<actuator-dcmotor-motorconst>`



`resistance<actuator-dcmotor-resistance>`



`nominal<actuator-dcmotor-nominal>`



`saturation<actuator-dcmotor-saturation>`



`inductance<actuator-dcmotor-inductance>`



`cogging<actuator-dcmotor-cogging>`



`controller<actuator-dcmotor-controller>`



`thermal<actuator-dcmotor-thermal>`



`lugre<actuator-dcmotor-lugre>`



`input<actuator-dcmotor-input>`





`plugin<actuator-plugin>` ​


2 3 4 4


`name<actuator-plugin-name>`



`class<actuator-plugin-class>`



`group<actuator-plugin-group>`



`nsample<actuator-plugin-nsample>`



`interp<actuator-plugin-interp>`



`delay<actuator-plugin-delay>`



`ctrlrange<actuator-plugin-ctrlrange>`



`user<actuator-plugin-user>`



`plugin<actuator-plugin-plugin>`



`instance<actuator-plugin-instance>`



`ctrllimited<actuator-plugin-ctrllimited>`



`forcelimited<actuator-plugin-forcelimited>`



`actlimited<actuator-plugin-actlimited>`



`forcerange<actuator-plugin-forcerange>`



`actrange<actuator-plugin-actrange>`



`lengthrange<actuator-plugin-lengthrange>`



`gear<actuator-plugin-gear>`



`damping<actuator-plugin-damping>`



`armature<actuator-plugin-armature>`



`cranklength<actuator-plugin-cranklength>`



`joint<actuator-plugin-joint>`



`jointinparent<actuator-plugin-jointinparent>`



`site<actuator-plugin-site>`



`actdim<actuator-plugin-actdim>`



`dyntype<actuator-plugin-dyntype>`



`dynprm<actuator-plugin-dynprm>`



`tendon<actuator-plugin-tendon>`



`cranksite<actuator-plugin-cranksite>`



`slidersite<actuator-plugin-slidersite>`



`actearly<actuator-plugin-actearly>`




`config<plugin-config>` ​


2 3 4 4


`key<plugin-config-key>`



`value<plugin-config-value>`







`sensor<sensor>` ​


`touch<sensor-touch>` ​


2 3 4 4


`name<sensor-touch-name>`



`nsample<sensor-touch-nsample>`



`interp<sensor-touch-interp>`



`delay<sensor-touch-delay>`



`interval<sensor-touch-interval>`



`cutoff<sensor-touch-cutoff>`



`noise<sensor-touch-noise>`



`user<sensor-touch-user>`



`site<sensor-touch-site>`





`accelerometer<sensor-accelerometer>` ​


2 3 4 4


`name<sensor-accelerometer-name>`



`nsample<sensor-accelerometer-nsample>`



`interp<sensor-accelerometer-interp>`



`delay<sensor-accelerometer-delay>`



`interval<sensor-accelerometer-interval>`



`cutoff<sensor-accelerometer-cutoff>`



`noise<sensor-accelerometer-noise>`



`user<sensor-accelerometer-user>`



`site<sensor-accelerometer-site>`





`velocimeter<sensor-velocimeter>` ​


2 3 4 4


`name<sensor-velocimeter-name>`



`nsample<sensor-velocimeter-nsample>`



`interp<sensor-velocimeter-interp>`



`delay<sensor-velocimeter-delay>`



`interval<sensor-velocimeter-interval>`



`cutoff<sensor-velocimeter-cutoff>`



`noise<sensor-velocimeter-noise>`



`user<sensor-velocimeter-user>`



`site<sensor-velocimeter-site>`





`gyro<sensor-gyro>` ​


2 3 4 4


`name<sensor-gyro-name>`



`nsample<sensor-gyro-nsample>`



`interp<sensor-gyro-interp>`



`delay<sensor-gyro-delay>`



`interval<sensor-gyro-interval>`



`cutoff<sensor-gyro-cutoff>`



`noise<sensor-gyro-noise>`



`user<sensor-gyro-user>`



`site<sensor-gyro-site>`





`force<sensor-force>` ​


2 3 4 4


`name<sensor-force-name>`



`nsample<sensor-force-nsample>`



`interp<sensor-force-interp>`



`delay<sensor-force-delay>`



`interval<sensor-force-interval>`



`cutoff<sensor-force-cutoff>`



`noise<sensor-force-noise>`



`user<sensor-force-user>`



`site<sensor-force-site>`





`torque<sensor-torque>` ​


2 3 4 4


`name<sensor-torque-name>`



`nsample<sensor-torque-nsample>`



`interp<sensor-torque-interp>`



`delay<sensor-torque-delay>`



`interval<sensor-torque-interval>`



`cutoff<sensor-torque-cutoff>`



`noise<sensor-torque-noise>`



`user<sensor-torque-user>`



`site<sensor-torque-site>`





`magnetometer<sensor-magnetometer>` ​


2 3 4 4


`name<sensor-magnetometer-name>`



`nsample<sensor-magnetometer-nsample>`



`interp<sensor-magnetometer-interp>`



`delay<sensor-magnetometer-delay>`



`interval<sensor-magnetometer-interval>`



`cutoff<sensor-magnetometer-cutoff>`



`noise<sensor-magnetometer-noise>`



`user<sensor-magnetometer-user>`



`site<sensor-magnetometer-site>`





`camprojection<sensor-camprojection>` ​


2 3 4 4


`name<sensor-camprojection-name>`



`nsample<sensor-camprojection-nsample>`



`interp<sensor-camprojection-interp>`



`delay<sensor-camprojection-delay>`



`interval<sensor-camprojection-interval>`



`cutoff<sensor-camprojection-cutoff>`



`noise<sensor-camprojection-noise>`



`user<sensor-camprojection-user>`



`site<sensor-camprojection-site>`



`camera<sensor-camprojection-camera>`





`rangefinder<sensor-rangefinder>` ​


2 3 4 4


`name<sensor-rangefinder-name>`



`nsample<sensor-rangefinder-nsample>`



`interp<sensor-rangefinder-interp>`



`delay<sensor-rangefinder-delay>`



`interval<sensor-rangefinder-interval>`



`cutoff<sensor-rangefinder-cutoff>`



`noise<sensor-rangefinder-noise>`



`user<sensor-rangefinder-user>`



`site<sensor-rangefinder-site>`



`camera<sensor-rangefinder-camera>`



`data<sensor-rangefinder-data>`





`jointpos<sensor-jointpos>` ​


2 3 4 4


`name<sensor-jointpos-name>`



`nsample<sensor-jointpos-nsample>`



`interp<sensor-jointpos-interp>`



`delay<sensor-jointpos-delay>`



`interval<sensor-jointpos-interval>`



`cutoff<sensor-jointpos-cutoff>`



`noise<sensor-jointpos-noise>`



`user<sensor-jointpos-user>`



`joint<sensor-jointpos-joint>`





`jointvel<sensor-jointvel>` ​


2 3 4 4


`name<sensor-jointvel-name>`



`nsample<sensor-jointvel-nsample>`



`interp<sensor-jointvel-interp>`



`delay<sensor-jointvel-delay>`



`interval<sensor-jointvel-interval>`



`cutoff<sensor-jointvel-cutoff>`



`noise<sensor-jointvel-noise>`



`user<sensor-jointvel-user>`



`joint<sensor-jointvel-joint>`





`tendonpos<sensor-tendonpos>` ​


2 3 4 4


`name<sensor-tendonpos-name>`



`nsample<sensor-tendonpos-nsample>`



`interp<sensor-tendonpos-interp>`



`delay<sensor-tendonpos-delay>`



`interval<sensor-tendonpos-interval>`



`cutoff<sensor-tendonpos-cutoff>`



`noise<sensor-tendonpos-noise>`



`user<sensor-tendonpos-user>`



`tendon<sensor-tendonpos-tendon>`





`tendonvel<sensor-tendonvel>` ​


2 3 4 4


`name<sensor-tendonvel-name>`



`nsample<sensor-tendonvel-nsample>`



`interp<sensor-tendonvel-interp>`



`delay<sensor-tendonvel-delay>`



`interval<sensor-tendonvel-interval>`



`cutoff<sensor-tendonvel-cutoff>`



`noise<sensor-tendonvel-noise>`



`user<sensor-tendonvel-user>`



`tendon<sensor-tendonvel-tendon>`





`actuatorpos<sensor-actuatorpos>` ​


2 3 4 4


`name<sensor-actuatorpos-name>`



`nsample<sensor-actuatorpos-nsample>`



`interp<sensor-actuatorpos-interp>`



`delay<sensor-actuatorpos-delay>`



`interval<sensor-actuatorpos-interval>`



`cutoff<sensor-actuatorpos-cutoff>`



`noise<sensor-actuatorpos-noise>`



`user<sensor-actuatorpos-user>`



`actuator<sensor-actuatorpos-actuator>`





`actuatorvel<sensor-actuatorvel>` ​


2 3 4 4


`name<sensor-actuatorvel-name>`



`nsample<sensor-actuatorvel-nsample>`



`interp<sensor-actuatorvel-interp>`



`delay<sensor-actuatorvel-delay>`



`interval<sensor-actuatorvel-interval>`



`cutoff<sensor-actuatorvel-cutoff>`



`noise<sensor-actuatorvel-noise>`



`user<sensor-actuatorvel-user>`



`actuator<sensor-actuatorvel-actuator>`





`actuatorfrc<sensor-actuatorfrc>` ​


2 3 4 4


`name<sensor-actuatorfrc-name>`



`nsample<sensor-actuatorfrc-nsample>`



`interp<sensor-actuatorfrc-interp>`



`delay<sensor-actuatorfrc-delay>`



`interval<sensor-actuatorfrc-interval>`



`cutoff<sensor-actuatorfrc-cutoff>`



`noise<sensor-actuatorfrc-noise>`



`user<sensor-actuatorfrc-user>`



`actuator<sensor-actuatorfrc-actuator>`





`jointactuatorfrc<sensor-jointactuatorfrc>` ​


2 3 4 4


`name<sensor-jointactuatorfrc-name>`



`nsample<sensor-jointactuatorfrc-nsample>`



`interp<sensor-jointactuatorfrc-interp>`



`delay<sensor-jointactuatorfrc-delay>`



`interval<sensor-jointactuatorfrc-interval>`



`cutoff<sensor-jointactuatorfrc-cutoff>`



`noise<sensor-jointactuatorfrc-noise>`



`user<sensor-jointactuatorfrc-user>`



`joint<sensor-jointactuatorfrc-joint>`





`tendonactuatorfrc<sensor-tendonactuatorfrc>` ​


2 3 4 4


`name<sensor-tendonactuatorfrc-name>`



`nsample<sensor-tendonactuatorfrc-nsample>`



`interp<sensor-tendonactuatorfrc-interp>`



`delay<sensor-tendonactuatorfrc-delay>`



`interval<sensor-tendonactuatorfrc-interval>`



`cutoff<sensor-tendonactuatorfrc-cutoff>`



`noise<sensor-tendonactuatorfrc-noise>`



`user<sensor-tendonactuatorfrc-user>`



`tendon<sensor-tendonactuatorfrc-tendon>`





`ballquat<sensor-ballquat>` ​


2 3 4 4


`name<sensor-ballquat-name>`



`nsample<sensor-ballquat-nsample>`



`interp<sensor-ballquat-interp>`



`delay<sensor-ballquat-delay>`



`interval<sensor-ballquat-interval>`



`cutoff<sensor-ballquat-cutoff>`



`noise<sensor-ballquat-noise>`



`user<sensor-ballquat-user>`



`joint<sensor-ballquat-joint>`





`ballangvel<sensor-ballangvel>` ​


2 3 4 4


`name<sensor-ballangvel-name>`



`nsample<sensor-ballangvel-nsample>`



`interp<sensor-ballangvel-interp>`



`delay<sensor-ballangvel-delay>`



`interval<sensor-ballangvel-interval>`



`cutoff<sensor-ballangvel-cutoff>`



`noise<sensor-ballangvel-noise>`



`user<sensor-ballangvel-user>`



`joint<sensor-ballangvel-joint>`





`jointlimitpos<sensor-jointlimitpos>` ​


2 3 4 4


`name<sensor-jointlimitpos-name>`



`nsample<sensor-jointlimitpos-nsample>`



`interp<sensor-jointlimitpos-interp>`



`delay<sensor-jointlimitpos-delay>`



`interval<sensor-jointlimitpos-interval>`



`cutoff<sensor-jointlimitpos-cutoff>`



`noise<sensor-jointlimitpos-noise>`



`user<sensor-jointlimitpos-user>`



`joint<sensor-jointlimitpos-joint>`





`jointlimitvel<sensor-jointlimitvel>` ​


2 3 4 4


`name<sensor-jointlimitvel-name>`



`nsample<sensor-jointlimitvel-nsample>`



`interp<sensor-jointlimitvel-interp>`



`delay<sensor-jointlimitvel-delay>`



`interval<sensor-jointlimitvel-interval>`



`cutoff<sensor-jointlimitvel-cutoff>`



`noise<sensor-jointlimitvel-noise>`



`user<sensor-jointlimitvel-user>`



`joint<sensor-jointlimitvel-joint>`





`jointlimitfrc<sensor-jointlimitfrc>` ​


2 3 4 4


`name<sensor-jointlimitfrc-name>`



`nsample<sensor-jointlimitfrc-nsample>`



`interp<sensor-jointlimitfrc-interp>`



`delay<sensor-jointlimitfrc-delay>`



`interval<sensor-jointlimitfrc-interval>`



`cutoff<sensor-jointlimitfrc-cutoff>`



`noise<sensor-jointlimitfrc-noise>`



`user<sensor-jointlimitfrc-user>`



`joint<sensor-jointlimitfrc-joint>`





`tendonlimitpos<sensor-tendonlimitpos>` ​


2 3 4 4


`name<sensor-tendonlimitpos-name>`



`nsample<sensor-tendonlimitpos-nsample>`



`interp<sensor-tendonlimitpos-interp>`



`delay<sensor-tendonlimitpos-delay>`



`interval<sensor-tendonlimitpos-interval>`



`cutoff<sensor-tendonlimitpos-cutoff>`



`noise<sensor-tendonlimitpos-noise>`



`user<sensor-tendonlimitpos-user>`



`tendon<sensor-tendonlimitpos-tendon>`





`tendonlimitvel<sensor-tendonlimitvel>` ​


2 3 4 4


`name<sensor-tendonlimitvel-name>`



`nsample<sensor-tendonlimitvel-nsample>`



`interp<sensor-tendonlimitvel-interp>`



`delay<sensor-tendonlimitvel-delay>`



`interval<sensor-tendonlimitvel-interval>`



`cutoff<sensor-tendonlimitvel-cutoff>`



`noise<sensor-tendonlimitvel-noise>`



`user<sensor-tendonlimitvel-user>`



`tendon<sensor-tendonlimitvel-tendon>`





`tendonlimitfrc<sensor-tendonlimitfrc>` ​


2 3 4 4


`name<sensor-tendonlimitfrc-name>`



`nsample<sensor-tendonlimitfrc-nsample>`



`interp<sensor-tendonlimitfrc-interp>`



`delay<sensor-tendonlimitfrc-delay>`



`interval<sensor-tendonlimitfrc-interval>`



`cutoff<sensor-tendonlimitfrc-cutoff>`



`noise<sensor-tendonlimitfrc-noise>`



`user<sensor-tendonlimitfrc-user>`



`tendon<sensor-tendonlimitfrc-tendon>`





`framepos<sensor-framepos>` ​


2 3 4 4


`name<sensor-framepos-name>`



`nsample<sensor-framepos-nsample>`



`interp<sensor-framepos-interp>`



`delay<sensor-framepos-delay>`



`interval<sensor-framepos-interval>`



`cutoff<sensor-framepos-cutoff>`



`noise<sensor-framepos-noise>`



`user<sensor-framepos-user>`



`objtype<sensor-framepos-objtype>`



`objname<sensor-framepos-objname>`



`reftype<sensor-framepos-reftype>`



`refname<sensor-framepos-refname>`





`framequat<sensor-framequat>` ​


2 3 4 4


`name<sensor-framequat-name>`



`nsample<sensor-framequat-nsample>`



`interp<sensor-framequat-interp>`



`delay<sensor-framequat-delay>`



`interval<sensor-framequat-interval>`



`cutoff<sensor-framequat-cutoff>`



`noise<sensor-framequat-noise>`



`user<sensor-framequat-user>`



`objtype<sensor-framequat-objtype>`



`objname<sensor-framequat-objname>`



`reftype<sensor-framequat-reftype>`



`refname<sensor-framequat-refname>`





`framexaxis<sensor-framexaxis>` ​


2 3 4 4


`name<sensor-framexaxis-name>`



`nsample<sensor-framexaxis-nsample>`



`interp<sensor-framexaxis-interp>`



`delay<sensor-framexaxis-delay>`



`interval<sensor-framexaxis-interval>`



`cutoff<sensor-framexaxis-cutoff>`



`noise<sensor-framexaxis-noise>`



`user<sensor-framexaxis-user>`



`objtype<sensor-framexaxis-objtype>`



`objname<sensor-framexaxis-objname>`



`reftype<sensor-framexaxis-reftype>`



`refname<sensor-framexaxis-refname>`





`frameyaxis<sensor-frameyaxis>` ​


2 3 4 4


`name<sensor-frameyaxis-name>`



`nsample<sensor-frameyaxis-nsample>`



`interp<sensor-frameyaxis-interp>`



`delay<sensor-frameyaxis-delay>`



`interval<sensor-frameyaxis-interval>`



`cutoff<sensor-frameyaxis-cutoff>`



`noise<sensor-frameyaxis-noise>`



`user<sensor-frameyaxis-user>`



`objtype<sensor-frameyaxis-objtype>`



`objname<sensor-frameyaxis-objname>`



`reftype<sensor-frameyaxis-reftype>`



`refname<sensor-frameyaxis-refname>`





`framezaxis<sensor-framezaxis>` ​


2 3 4 4


`name<sensor-framezaxis-name>`



`nsample<sensor-framezaxis-nsample>`



`interp<sensor-framezaxis-interp>`



`delay<sensor-framezaxis-delay>`



`interval<sensor-framezaxis-interval>`



`cutoff<sensor-framezaxis-cutoff>`



`noise<sensor-framezaxis-noise>`



`user<sensor-framezaxis-user>`



`objtype<sensor-framezaxis-objtype>`



`objname<sensor-framezaxis-objname>`



`reftype<sensor-framezaxis-reftype>`



`refname<sensor-framezaxis-refname>`





`framelinvel<sensor-framelinvel>` ​


2 3 4 4


`name<sensor-framelinvel-name>`



`nsample<sensor-framelinvel-nsample>`



`interp<sensor-framelinvel-interp>`



`delay<sensor-framelinvel-delay>`



`interval<sensor-framelinvel-interval>`



`cutoff<sensor-framelinvel-cutoff>`



`noise<sensor-framelinvel-noise>`



`user<sensor-framelinvel-user>`



`objtype<sensor-framelinvel-objtype>`



`objname<sensor-framelinvel-objname>`



`reftype<sensor-framelinvel-reftype>`



`refname<sensor-framelinvel-refname>`





`frameangvel<sensor-frameangvel>` ​


2 3 4 4


`name<sensor-frameangvel-name>`



`nsample<sensor-frameangvel-nsample>`



`interp<sensor-frameangvel-interp>`



`delay<sensor-frameangvel-delay>`



`interval<sensor-frameangvel-interval>`



`cutoff<sensor-frameangvel-cutoff>`



`noise<sensor-frameangvel-noise>`



`user<sensor-frameangvel-user>`



`objtype<sensor-frameangvel-objtype>`



`objname<sensor-frameangvel-objname>`



`reftype<sensor-frameangvel-reftype>`



`refname<sensor-frameangvel-refname>`





`framelinacc<sensor-framelinacc>` ​


2 3 4 4


`name<sensor-framelinacc-name>`



`nsample<sensor-framelinacc-nsample>`



`interp<sensor-framelinacc-interp>`



`delay<sensor-framelinacc-delay>`



`interval<sensor-framelinacc-interval>`



`cutoff<sensor-framelinacc-cutoff>`



`noise<sensor-framelinacc-noise>`



`user<sensor-framelinacc-user>`



`objtype<sensor-framelinacc-objtype>`



`objname<sensor-framelinacc-objname>`





`frameangacc<sensor-frameangacc>` ​


2 3 4 4


`name<sensor-frameangacc-name>`



`nsample<sensor-frameangacc-nsample>`



`interp<sensor-frameangacc-interp>`



`delay<sensor-frameangacc-delay>`



`interval<sensor-frameangacc-interval>`



`cutoff<sensor-frameangacc-cutoff>`



`noise<sensor-frameangacc-noise>`



`user<sensor-frameangacc-user>`



`objtype<sensor-frameangacc-objtype>`



`objname<sensor-frameangacc-objname>`





`subtreecom<sensor-subtreecom>` ​


2 3 4 4


`name<sensor-subtreecom-name>`



`nsample<sensor-subtreecom-nsample>`



`interp<sensor-subtreecom-interp>`



`delay<sensor-subtreecom-delay>`



`interval<sensor-subtreecom-interval>`



`cutoff<sensor-subtreecom-cutoff>`



`noise<sensor-subtreecom-noise>`



`user<sensor-subtreecom-user>`



`body<sensor-subtreecom-body>`





`subtreelinvel<sensor-subtreelinvel>` ​


2 3 4 4


`name<sensor-subtreelinvel-name>`



`nsample<sensor-subtreelinvel-nsample>`



`interp<sensor-subtreelinvel-interp>`



`delay<sensor-subtreelinvel-delay>`



`interval<sensor-subtreelinvel-interval>`



`cutoff<sensor-subtreelinvel-cutoff>`



`noise<sensor-subtreelinvel-noise>`



`user<sensor-subtreelinvel-user>`



`body<sensor-subtreelinvel-body>`





`subtreeangmom<sensor-subtreeangmom>` ​


2 3 4 4


`name<sensor-subtreeangmom-name>`



`nsample<sensor-subtreeangmom-nsample>`



`interp<sensor-subtreeangmom-interp>`



`delay<sensor-subtreeangmom-delay>`



`interval<sensor-subtreeangmom-interval>`



`cutoff<sensor-subtreeangmom-cutoff>`



`noise<sensor-subtreeangmom-noise>`



`user<sensor-subtreeangmom-user>`



`body<sensor-subtreeangmom-body>`





`insidesite<sensor-insidesite>` ​


2 3 4 4


`name<sensor-insidesite-name>`



`nsample<sensor-insidesite-nsample>`



`interp<sensor-insidesite-interp>`



`delay<sensor-insidesite-delay>`



`interval<sensor-insidesite-interval>`



`cutoff<sensor-insidesite-cutoff>`



`noise<sensor-insidesite-noise>`



`user<sensor-insidesite-user>`



`site<sensor-insidesite-site>`



`objtype<sensor-insidesite-objtype>`



`objname<sensor-insidesite-objname>`



`enclosed<sensor-insidesite-enclosed>`





`distance<sensor-distance>` ​


2 3 4 4


`name<sensor-distance-name>`



`nsample<sensor-distance-nsample>`



`interp<sensor-distance-interp>`



`delay<sensor-distance-delay>`



`interval<sensor-distance-interval>`



`cutoff<sensor-distance-cutoff>`



`noise<sensor-distance-noise>`



`user<sensor-distance-user>`



`geom1<sensor-distance-geom1>`



`geom2<sensor-distance-geom2>`



`body1<sensor-distance-body1>`



`body2<sensor-distance-body2>`





`normal<sensor-normal>` ​


2 3 4 4


`name<sensor-normal-name>`



`nsample<sensor-normal-nsample>`



`interp<sensor-normal-interp>`



`delay<sensor-normal-delay>`



`interval<sensor-normal-interval>`



`cutoff<sensor-normal-cutoff>`



`noise<sensor-normal-noise>`



`user<sensor-normal-user>`



`geom1<sensor-normal-geom1>`



`geom2<sensor-normal-geom2>`



`body1<sensor-normal-body1>`



`body2<sensor-normal-body2>`





`fromto<sensor-fromto>` ​


2 3 4 4


`name<sensor-fromto-name>`



`nsample<sensor-fromto-nsample>`



`interp<sensor-fromto-interp>`



`delay<sensor-fromto-delay>`



`interval<sensor-fromto-interval>`



`cutoff<sensor-fromto-cutoff>`



`noise<sensor-fromto-noise>`



`user<sensor-fromto-user>`



`geom1<sensor-fromto-geom1>`



`geom2<sensor-fromto-geom2>`



`body1<sensor-fromto-body1>`



`body2<sensor-fromto-body2>`





`contact<sensor-contact>` ​


2 3 4 4


`name<sensor-contact-name>`



`nsample<sensor-contact-nsample>`



`interp<sensor-contact-interp>`



`delay<sensor-contact-delay>`



`interval<sensor-contact-interval>`



`cutoff<sensor-contact-cutoff>`



`noise<sensor-contact-noise>`



`user<sensor-contact-user>`



`geom1<sensor-contact-geom1>`



`geom2<sensor-contact-geom2>`



`body1<sensor-contact-body1>`



`body2<sensor-contact-body2>`



`subtree1<sensor-contact-subtree1>`



`subtree2<sensor-contact-subtree2>`



`site<sensor-contact-site>`



`num<sensor-contact-num>`



`data<sensor-contact-data>`



`reduce<sensor-contact-reduce>`





`e_potential<sensor-e_potential>` ​


2 3 4 4


`name<sensor-e_potential-name>`



`nsample<sensor-e_potential-nsample>`



`interp<sensor-e_potential-interp>`



`delay<sensor-e_potential-delay>`



`interval<sensor-e_potential-interval>`



`cutoff<sensor-e_potential-cutoff>`



`noise<sensor-e_potential-noise>`



`user<sensor-e_potential-user>`





`e_kinetic<sensor-e_kinetic>` ​


2 3 4 4


`name<sensor-e_kinetic-name>`



`nsample<sensor-e_kinetic-nsample>`



`interp<sensor-e_kinetic-interp>`



`delay<sensor-e_kinetic-delay>`



`interval<sensor-e_kinetic-interval>`



`cutoff<sensor-e_kinetic-cutoff>`



`noise<sensor-e_kinetic-noise>`



`user<sensor-e_kinetic-user>`





`clock<sensor-clock>` ​


2 3 4 4


`name<sensor-clock-name>`



`nsample<sensor-clock-nsample>`



`interp<sensor-clock-interp>`



`delay<sensor-clock-delay>`



`interval<sensor-clock-interval>`



`cutoff<sensor-clock-cutoff>`



`noise<sensor-clock-noise>`



`user<sensor-clock-user>`





`tactile<sensor-tactile>` ​


2 3 4 4


`name<sensor-tactile-name>`



`geom<sensor-tactile-geom>`



`mesh<sensor-tactile-mesh>`



`nsample<sensor-tactile-nsample>`



`interp<sensor-tactile-interp>`



`delay<sensor-tactile-delay>`



`interval<sensor-tactile-interval>`



`cutoff<sensor-tactile-cutoff>`



`user<sensor-tactile-user>`





`user<sensor-user>` ​


2 3 4 4


`name<sensor-user-name>`



`objtype<sensor-user-objtype>`



`objname<sensor-user-objname>`



`datatype<sensor-user-datatype>`



`needstage<sensor-user-needstage>`



`dim<sensor-user-dim>`



`cutoff<sensor-user-cutoff>`



`noise<sensor-user-noise>`



`user<sensor-user-user>`





`plugin<sensor-plugin>` ​


2 3 4 4


`name<sensor-plugin-name>`



`plugin<sensor-plugin-plugin>`



`instance<sensor-plugin-instance>`



`cutoff<sensor-plugin-cutoff>`



`objtype<sensor-plugin-objtype>`



`objname<sensor-plugin-objname>`



`reftype<sensor-plugin-reftype>`



`refname<sensor-plugin-refname>`



`user<sensor-plugin-user>`




`config<plugin-config>` ​


2 3 4 4


`key<plugin-config-key>`



`value<plugin-config-value>`







`keyframe<keyframe>` ​


`key<keyframe-key>` ​


2 3 4 4


`name<keyframe-key-name>`



`time<keyframe-key-time>`



`qpos<keyframe-key-qpos>`



`qvel<keyframe-key-qvel>`



`act<keyframe-key-act>`



`mpos<keyframe-key-mpos>`



`mquat<keyframe-key-mquat>`



`ctrl<keyframe-key-ctrl>`



`plastic<keyframe-key-plastic>`






`visual<visual>` ​


`global<visual-global>` `dot`


2 3 4 4


`cameraid<visual-global-cameraid>`



`orthographic<visual-global-orthographic>`



`fovy<visual-global-fovy>`



`ipd<visual-global-ipd>`



`azimuth<visual-global-azimuth>`



`elevation<visual-global-elevation>`



`linewidth<visual-global-linewidth>`



`glow<visual-global-glow>`



`offwidth<visual-global-offwidth>`



`offheight<visual-global-offheight>`



`realtime<visual-global-realtime>`



`ellipsoidinertia<visual-global-ellipsoidinertia>`



`bvactive<visual-global-bvactive>`





`quality<visual-quality>` `dot`


2 3 4 4


`shadowsize<visual-quality-shadowsize>`



`offsamples<visual-quality-offsamples>`



`numslices<visual-quality-numslices>`



`numstacks<visual-quality-numstacks>`



`numquads<visual-quality-numquads>`





`headlight<visual-headlight>` `dot`


2 3 4 4


`ambient<visual-headlight-ambient>`



`diffuse<visual-headlight-diffuse>`



`specular<visual-headlight-specular>`



`active<visual-headlight-active>`





`map<visual-map>` `dot`


2 3 4 4


`stiffness<visual-map-stiffness>`



`stiffnessrot<visual-map-stiffnessrot>`



`force<visual-map-force>`



`torque<visual-map-torque>`



`alpha<visual-map-alpha>`



`fogstart<visual-map-fogstart>`



`fogend<visual-map-fogend>`



`znear<visual-map-znear>`



`zfar<visual-map-zfar>`



`haze<visual-map-haze>`



`shadowclip<visual-map-shadowclip>`



`shadowscale<visual-map-shadowscale>`



`actuatortendon<visual-map-actuatortendon>`





`scale<visual-scale>` `dot`


2 3 4 4


`forcewidth<visual-scale-forcewidth>`



`contactwidth<visual-scale-contactwidth>`



`contactheight<visual-scale-contactheight>`



`connect<visual-scale-connect>`



`com<visual-scale-com>`



`camera<visual-scale-camera>`



`light<visual-scale-light>`



`selectpoint<visual-scale-selectpoint>`



`jointlength<visual-scale-jointlength>`



`jointwidth<visual-scale-jointwidth>`



`actuatorlength<visual-scale-actuatorlength>`



`actuatorwidth<visual-scale-actuatorwidth>`



`framelength<visual-scale-framelength>`



`framewidth<visual-scale-framewidth>`



`constraint<visual-scale-constraint>`



`slidercrank<visual-scale-slidercrank>`



`frustum<visual-scale-frustum>`





`rgba<visual-rgba>` `dot`


2 3 4 4


`fog<visual-rgba-fog>`



`haze<visual-rgba-haze>`



`force<visual-rgba-force>`



`inertia<visual-rgba-inertia>`



`joint<visual-rgba-joint>`



`actuator<visual-rgba-actuator>`



`actuatornegative<visual-rgba-actuatornegative>`



`actuatorpositive<visual-rgba-actuatorpositive>`



`com<visual-rgba-com>`



`camera<visual-rgba-camera>`



`light<visual-rgba-light>`



`selectpoint<visual-rgba-selectpoint>`



`connect<visual-rgba-connect>`



`contactpoint<visual-rgba-contactpoint>`



`contactforce<visual-rgba-contactforce>`



`contactfriction<visual-rgba-contactfriction>`



`contacttorque<visual-rgba-contacttorque>`



`contactgap<visual-rgba-contactgap>`



`rangefinder<visual-rgba-rangefinder>`



`constraint<visual-rgba-constraint>`



`slidercrank<visual-rgba-slidercrank>`



`crankbroken<visual-rgba-crankbroken>`



`frustum<visual-rgba-frustum>`



`bv<visual-rgba-bv>`



`bvactive<visual-rgba-bvactive>`






`default<default>` `sync`


2 3 4 4


`class<default-class>`




`mesh<default-mesh>` `dot`


2 3 4 4


`scale<default-mesh-scale>`



`maxhullvert<default-mesh-maxhullvert>`



`inertia<default-mesh-inertia>`





`texture<default-texture>` `dot`


2 3 4 4


`type<default-texture-type>`



`colorspace<default-texture-colorspace>`



`gridsize<default-texture-gridsize>`



`gridlayout<default-texture-gridlayout>`



`builtin<default-texture-builtin>`



`rgb1<default-texture-rgb1>`



`rgb2<default-texture-rgb2>`



`mark<default-texture-mark>`



`markrgb<default-texture-markrgb>`



`random<default-texture-random>`



`width<default-texture-width>`



`height<default-texture-height>`



`hflip<default-texture-hflip>`



`vflip<default-texture-vflip>`



`nchannel<default-texture-nchannel>`



`embed<default-texture-embed>`





`material<default-material>` `dot`


2 3 4 4


`texture<default-material-texture>`



`texrepeat<default-material-texrepeat>`



`texuniform<default-material-texuniform>`



`emission<default-material-emission>`



`specular<default-material-specular>`



`shininess<default-material-shininess>`



`reflectance<default-material-reflectance>`



`metallic<default-material-metallic>`



`roughness<default-material-roughness>`



`rgba<default-material-rgba>`




`layer<material-layer>` ​


2 3 4 4


`texture<material-layer-texture>`



`role<material-layer-role>`






`joint<default-joint>` `dot`


2 3 4 4


`type<default-joint-type>`



`group<default-joint-group>`



`pos<default-joint-pos>`



`axis<default-joint-axis>`



`springdamper<default-joint-springdamper>`



`limited<default-joint-limited>`



`actuatorfrclimited<default-joint-actuatorfrclimited>`



`solreflimit<default-joint-solreflimit>`



`solimplimit<default-joint-solimplimit>`



`solreffriction<default-joint-solreffriction>`



`solimpfriction<default-joint-solimpfriction>`



`stiffness<default-joint-stiffness>`



`range<default-joint-range>`



`actuatorfrcrange<default-joint-actuatorfrcrange>`



`actuatorgravcomp<default-joint-actuatorgravcomp>`



`margin<default-joint-margin>`



`ref<default-joint-ref>`



`springref<default-joint-springref>`



`springyield<default-joint-springyield>`



`armature<default-joint-armature>`



`damping<default-joint-damping>`



`frictionloss<default-joint-frictionloss>`



`user<default-joint-user>`





`geom<default-geom>` `dot`


2 3 4 4


`type<default-geom-type>`



`contype<default-geom-contype>`



`conaffinity<default-geom-conaffinity>`



`condim<default-geom-condim>`



`group<default-geom-group>`



`priority<default-geom-priority>`



`size<default-geom-size>`



`material<default-geom-material>`



`friction<default-geom-friction>`



`mass<default-geom-mass>`



`density<default-geom-density>`



`shellinertia<default-geom-shellinertia>`



`solmix<default-geom-solmix>`



`solref<default-geom-solref>`



`solimp<default-geom-solimp>`



`margin<default-geom-margin>`



`gap<default-geom-gap>`



`surfacevel<default-geom-surfacevel>`



`adhesion<default-geom-adhesion>`



`fromto<default-geom-fromto>`



`pos<default-geom-pos>`



`quat<default-geom-quat>`



`axisangle<default-geom-axisangle>`



`xyaxes<default-geom-xyaxes>`



`zaxis<default-geom-zaxis>`



`euler<default-geom-euler>`



`hfield<default-geom-hfield>`



`mesh<default-geom-mesh>`



`fitscale<default-geom-fitscale>`



`rgba<default-geom-rgba>`



`castshadow<default-geom-castshadow>`



`fluidshape<default-geom-fluidshape>`



`fluidcoef<default-geom-fluidcoef>`



`user<default-geom-user>`





`site<default-site>` `dot`


2 3 4 4


`type<default-site-type>`



`group<default-site-group>`



`pos<default-site-pos>`



`quat<default-site-quat>`



`axisangle<default-site-axisangle>`



`xyaxes<default-site-xyaxes>`



`zaxis<default-site-zaxis>`



`euler<default-site-euler>`



`material<default-site-material>`



`mesh<default-site-mesh>`



`size<default-site-size>`



`fromto<default-site-fromto>`



`rgba<default-site-rgba>`



`user<default-site-user>`





`camera<default-camera>` `dot`


2 3 4 4


`projection<default-camera-projection>`



`fovy<default-camera-fovy>`



`ipd<default-camera-ipd>`



`resolution<default-camera-resolution>`



`output<default-camera-output>`



`pos<default-camera-pos>`



`quat<default-camera-quat>`



`axisangle<default-camera-axisangle>`



`xyaxes<default-camera-xyaxes>`



`zaxis<default-camera-zaxis>`



`euler<default-camera-euler>`



`mode<default-camera-mode>`



`focal<default-camera-focal>`



`focalpixel<default-camera-focalpixel>`



`principal<default-camera-principal>`



`principalpixel<default-camera-principalpixel>`



`sensorsize<default-camera-sensorsize>`



`user<default-camera-user>`





`light<default-light>` `dot`


2 3 4 4


`directional<default-light-directional>`



`type<default-light-type>`



`castshadow<default-light-castshadow>`



`active<default-light-active>`



`pos<default-light-pos>`



`dir<default-light-dir>`



`bulbradius<default-light-bulbradius>`



`intensity<default-light-intensity>`



`range<default-light-range>`



`attenuation<default-light-attenuation>`



`cutoff<default-light-cutoff>`



`softness<default-light-softness>`



`exponent<default-light-exponent>`



`ambient<default-light-ambient>`



`diffuse<default-light-diffuse>`



`specular<default-light-specular>`



`mode<default-light-mode>`





`pair<default-pair>` `dot`


2 3 4 4


`condim<default-pair-condim>`



`friction<default-pair-friction>`



`solref<default-pair-solref>`



`solreffriction<default-pair-solreffriction>`



`solimp<default-pair-solimp>`



`gap<default-pair-gap>`



`margin<default-pair-margin>`



`adhesion<default-pair-adhesion>`





`equality<default-equality>` `dot`


2 3 4 4


`active<default-equality-active>`



`solref<default-equality-solref>`



`solimp<default-equality-solimp>`





`tendon<default-tendon>` `dot`


2 3 4 4


`group<default-tendon-group>`



`limited<default-tendon-limited>`



`actuatorfrclimited<default-tendon-actuatorfrclimited>`



`range<default-tendon-range>`



`actuatorfrcrange<default-tendon-actuatorfrcrange>`



`solreflimit<default-tendon-solreflimit>`



`solimplimit<default-tendon-solimplimit>`



`solreffriction<default-tendon-solreffriction>`



`solimpfriction<default-tendon-solimpfriction>`



`frictionloss<default-tendon-frictionloss>`



`springlength<default-tendon-springlength>`



`springyield<default-tendon-springyield>`



`width<default-tendon-width>`



`material<default-tendon-material>`



`margin<default-tendon-margin>`



`stiffness<default-tendon-stiffness>`



`damping<default-tendon-damping>`



`armature<default-tendon-armature>`



`rgba<default-tendon-rgba>`



`user<default-tendon-user>`





`general<default-general>` `dot`


2 3 4 4


`group<default-general-group>`



`nsample<default-general-nsample>`



`interp<default-general-interp>`



`delay<default-general-delay>`



`ctrlrange<default-general-ctrlrange>`



`user<default-general-user>`



`ctrllimited<default-general-ctrllimited>`



`forcelimited<default-general-forcelimited>`



`actlimited<default-general-actlimited>`



`forcerange<default-general-forcerange>`



`actrange<default-general-actrange>`



`gear<default-general-gear>`



`damping<default-general-damping>`



`armature<default-general-armature>`



`cranklength<default-general-cranklength>`



`actdim<default-general-actdim>`



`input<default-general-input>`



`velrange<default-general-velrange>`



`ffrange<default-general-ffrange>`



`inheritrange<default-general-inheritrange>`



`dyntype<default-general-dyntype>`



`gaintype<default-general-gaintype>`



`biastype<default-general-biastype>`



`dynprm<default-general-dynprm>`



`gainprm<default-general-gainprm>`



`biasprm<default-general-biasprm>`



`actearly<default-general-actearly>`





`motor<default-motor>` `dot`


2 3 4 4


`group<default-motor-group>`



`nsample<default-motor-nsample>`



`interp<default-motor-interp>`



`delay<default-motor-delay>`



`ctrlrange<default-motor-ctrlrange>`



`user<default-motor-user>`



`ctrllimited<default-motor-ctrllimited>`



`forcelimited<default-motor-forcelimited>`



`forcerange<default-motor-forcerange>`



`gear<default-motor-gear>`



`damping<default-motor-damping>`



`armature<default-motor-armature>`



`cranklength<default-motor-cranklength>`





`position<default-position>` `dot`


2 3 4 4


`group<default-position-group>`



`nsample<default-position-nsample>`



`interp<default-position-interp>`



`delay<default-position-delay>`



`ctrlrange<default-position-ctrlrange>`



`user<default-position-user>`



`ctrllimited<default-position-ctrllimited>`



`forcelimited<default-position-forcelimited>`



`inheritrange<default-position-inheritrange>`



`forcerange<default-position-forcerange>`



`gear<default-position-gear>`



`damping<default-position-damping>`



`armature<default-position-armature>`



`cranklength<default-position-cranklength>`



`kp<default-position-kp>`



`kv<default-position-kv>`



`dampratio<default-position-dampratio>`



`timeconst<default-position-timeconst>`





`velocity<default-velocity>` `dot`


2 3 4 4


`group<default-velocity-group>`



`nsample<default-velocity-nsample>`



`interp<default-velocity-interp>`



`delay<default-velocity-delay>`



`ctrlrange<default-velocity-ctrlrange>`



`user<default-velocity-user>`



`ctrllimited<default-velocity-ctrllimited>`



`forcelimited<default-velocity-forcelimited>`



`forcerange<default-velocity-forcerange>`



`gear<default-velocity-gear>`



`damping<default-velocity-damping>`



`armature<default-velocity-armature>`



`cranklength<default-velocity-cranklength>`



`kv<default-velocity-kv>`





`intvelocity<default-intvelocity>` `dot`


2 3 4 4


`group<default-intvelocity-group>`



`nsample<default-intvelocity-nsample>`



`interp<default-intvelocity-interp>`



`delay<default-intvelocity-delay>`



`ctrlrange<default-intvelocity-ctrlrange>`



`user<default-intvelocity-user>`



`ctrllimited<default-intvelocity-ctrllimited>`



`forcelimited<default-intvelocity-forcelimited>`



`actlimited<default-intvelocity-actlimited>`



`forcerange<default-intvelocity-forcerange>`



`actrange<default-intvelocity-actrange>`



`inheritrange<default-intvelocity-inheritrange>`



`gear<default-intvelocity-gear>`



`damping<default-intvelocity-damping>`



`armature<default-intvelocity-armature>`



`cranklength<default-intvelocity-cranklength>`



`kp<default-intvelocity-kp>`



`kv<default-intvelocity-kv>`



`dampratio<default-intvelocity-dampratio>`





`orientation<default-orientation>` `dot`


2 3 4 4


`group<default-orientation-group>`



`nsample<default-orientation-nsample>`



`interp<default-orientation-interp>`



`delay<default-orientation-delay>`



`ctrlrange<default-orientation-ctrlrange>`



`user<default-orientation-user>`



`forcelimited<default-orientation-forcelimited>`



`forcerange<default-orientation-forcerange>`



`kp<default-orientation-kp>`



`kv<default-orientation-kv>`



`dampratio<default-orientation-dampratio>`



`input<default-orientation-input>`





`pid<default-pid>` `dot`


2 3 4 4


`group<default-pid-group>`



`nsample<default-pid-nsample>`



`interp<default-pid-interp>`



`delay<default-pid-delay>`



`ctrlrange<default-pid-ctrlrange>`



`user<default-pid-user>`



`ctrllimited<default-pid-ctrllimited>`



`forcelimited<default-pid-forcelimited>`



`posrange<default-pid-posrange>`



`velrange<default-pid-velrange>`



`ffrange<default-pid-ffrange>`



`forcerange<default-pid-forcerange>`



`inheritrange<default-pid-inheritrange>`



`gear<default-pid-gear>`



`damping<default-pid-damping>`



`armature<default-pid-armature>`



`cranklength<default-pid-cranklength>`



`kp<default-pid-kp>`



`kv<default-pid-kv>`



`dampratio<default-pid-dampratio>`



`ki<default-pid-ki>`



`imax<default-pid-imax>`



`slewmax<default-pid-slewmax>`



`input<default-pid-input>`





`damper<default-damper>` `dot`


2 3 4 4


`group<default-damper-group>`



`nsample<default-damper-nsample>`



`interp<default-damper-interp>`



`delay<default-damper-delay>`



`ctrlrange<default-damper-ctrlrange>`



`user<default-damper-user>`



`forcelimited<default-damper-forcelimited>`



`forcerange<default-damper-forcerange>`



`gear<default-damper-gear>`



`damping<default-damper-damping>`



`armature<default-damper-armature>`



`cranklength<default-damper-cranklength>`



`kv<default-damper-kv>`





`cylinder<default-cylinder>` `dot`


2 3 4 4


`group<default-cylinder-group>`



`nsample<default-cylinder-nsample>`



`interp<default-cylinder-interp>`



`delay<default-cylinder-delay>`



`ctrlrange<default-cylinder-ctrlrange>`



`user<default-cylinder-user>`



`ctrllimited<default-cylinder-ctrllimited>`



`forcelimited<default-cylinder-forcelimited>`



`forcerange<default-cylinder-forcerange>`



`gear<default-cylinder-gear>`



`damping<default-cylinder-damping>`



`armature<default-cylinder-armature>`



`cranklength<default-cylinder-cranklength>`



`timeconst<default-cylinder-timeconst>`



`area<default-cylinder-area>`



`diameter<default-cylinder-diameter>`



`bias<default-cylinder-bias>`





`muscle<default-muscle>` `dot`


2 3 4 4


`group<default-muscle-group>`



`nsample<default-muscle-nsample>`



`interp<default-muscle-interp>`



`delay<default-muscle-delay>`



`ctrlrange<default-muscle-ctrlrange>`



`user<default-muscle-user>`



`ctrllimited<default-muscle-ctrllimited>`



`forcelimited<default-muscle-forcelimited>`



`forcerange<default-muscle-forcerange>`



`gear<default-muscle-gear>`



`damping<default-muscle-damping>`



`armature<default-muscle-armature>`



`cranklength<default-muscle-cranklength>`



`timeconst<default-muscle-timeconst>`



`range<default-muscle-range>`



`force<default-muscle-force>`



`scale<default-muscle-scale>`



`lmin<default-muscle-lmin>`



`lmax<default-muscle-lmax>`



`vmax<default-muscle-vmax>`



`fpmax<default-muscle-fpmax>`



`fvmax<default-muscle-fvmax>`





`adhesion<default-adhesion>` `dot`


2 3 4 4


`group<default-adhesion-group>`



`nsample<default-adhesion-nsample>`



`interp<default-adhesion-interp>`



`delay<default-adhesion-delay>`



`ctrlrange<default-adhesion-ctrlrange>`



`user<default-adhesion-user>`



`forcelimited<default-adhesion-forcelimited>`



`forcerange<default-adhesion-forcerange>`



`gain<default-adhesion-gain>`





`dcmotor<default-dcmotor>` `dot`


2 3 4 4


`group<default-dcmotor-group>`



`nsample<default-dcmotor-nsample>`



`interp<default-dcmotor-interp>`



`delay<default-dcmotor-delay>`



`ctrlrange<default-dcmotor-ctrlrange>`



`user<default-dcmotor-user>`



`ctrllimited<default-dcmotor-ctrllimited>`



`gear<default-dcmotor-gear>`



`damping<default-dcmotor-damping>`



`armature<default-dcmotor-armature>`



`cranklength<default-dcmotor-cranklength>`



`motorconst<default-dcmotor-motorconst>`



`resistance<default-dcmotor-resistance>`



`nominal<default-dcmotor-nominal>`



`saturation<default-dcmotor-saturation>`



`inductance<default-dcmotor-inductance>`



`cogging<default-dcmotor-cogging>`



`controller<default-dcmotor-controller>`



`thermal<default-dcmotor-thermal>`



`lugre<default-dcmotor-lugre>`



`input<default-dcmotor-input>`






`custom<custom>` ​


`numeric<custom-numeric>` ​


2 3 4 4


`name<custom-numeric-name>`



`size<custom-numeric-size>`



`data<custom-numeric-data>`





`text<custom-text>` ​


2 3 4 4


`name<custom-text-name>`



`data<custom-text-data>`





`tuple<custom-tuple>` ​


2 3 4 4


`name<custom-tuple-name>`




`element<tuple-element>` ​


2 3 4 4


`objtype<tuple-element-objtype>`



`objname<tuple-element-objname>`



`prm<tuple-element-prm>`







`extension<extension>` ​


`plugin<extension-plugin>` ​


2 3 4 4


`plugin<extension-plugin-plugin>`




`instance<plugin-instance>` ​


2 3 4 4


`name<plugin-instance-name>`




`config<instance-config>` ​


2 3 4 4


`key<instance-config-key>`



`value<instance-config-value>`











latex

> [!NOTE]
> The XML schema table is only available in the HTML version of this documentation.


### Attribute types

Each attribute has a data type enforced by the parser. The available data types are:

|  |  |
|----|----|
| string | An arbitrary string, usually specifying a file name or a user-defined name of a model element. |
| int(N) | An array of N integers. If N is omitted it equals 1. |
| real(N) | An array of N real-valued numbers. If N is omitted it equals 1. |
| \[...\] | Keyword attribute. The list of valid keywords is given in brackets. |

\
For array-type attributes, the length of the array is enforced by the parser unless specified otherwise in the reference documentation below.\
In addition to having a data type, attributes can be required or optional. Optional attributes can have internal defaults or not. Optional attributes that do not have internal defaults are initialized in a special undefined state. This state is different from any valid setting that can be entered in the XML. This mechanism enables the compiler to determine if the attribute has been "touched" by the user, either explicitly or through defaults, and take appropriate action. Some attributes have internal defaults (usually 0) which are not actually allowed by the compiler. When such attributes become relevant in a given context, they must be set to allowed values.

|  |  |
|----|----|
| required | The attribute is required by the parser. If it is not present the parser will generate an error. |
| optional | The attribute is optional. There is no internal default. The attribute is initialized in the undefined state. |
| "..." | The attribute is optional. The internal default is given in quotes. |

In the reference documentation below the attribute name is shown in boldface, followed by its data type, followed by the required/optional status including the internal default if any. For example, the attribute angle is a keyword attribute whose value can be "radian" or "degree". It is an optional attribute and has internal default "degree". Therefore it will appear in the reference documentation as

<span class="at">angle</span>: <span class="at-val">\[radian, degree\], "degree"</span>  
<p style="display: none"></p>

### Attribute dimensions

MuJoCo does not fix a system of units, see [Units are unspecified](overview.md). The table below gives the physical dimension of every real-valued attribute in terms of length $`L`$, mass $`M`$ and time $`T`$, and the symbols

|  |  |
|----|----|
| $`A`$ | Plane angle, dimensionless. Orientations and the <span class="at">range</span>, <span class="at">ref</span> and <span class="at">springref</span> of hinge and ball joints are read in the unit set by [compiler/angle](XMLreference.md). Other angles are radians, unless their description says otherwise. |
| $`Q`$ | The coordinate of the joint, tendon or actuator transmission: an angle for hinge and ball joints, a length for slide joints and spatial tendons. The coordinate of a [fixed tendon](XMLreference.md) is [coef](XMLreference.md) times the coordinates of its joints. |
| $`F`$ | The generalized force conjugate to $`Q`$, of dimension $`M\,L^2\,T^{-2}\,Q^{-1}`$: a torque when $`Q`$ is an angle, a force when it is a length. |

Integer attributes are counts, indices or flags, and dimensionless. Raw asset data is in the asset's own units: mesh <span class="at">vertex</span> and <span class="at">refpos</span> and flexcomp <span class="at">point</span> and <span class="at">origin</span> are dimensionless, and <span class="at">scale</span>, which converts them to lengths, has dimension $`L`$. A dimension marked *varies* depends on other attributes of the element, for example the outputs selected by a sensor's <span class="at">data</span>; *other* marks quantities not expressible in these terms, such as user data and the electrical parameters of [dcmotor](XMLreference.md).


Dimensions of all attributes

| Attribute | Dimension |
|----|----|
| `compiler/boundmass<compiler-boundmass>` | $`M`$ |
| `compiler/boundinertia<compiler-boundinertia>` | $`M\,L^{2}`$ |
| `compiler/settotalmass<compiler-settotalmass>` | $`M`$ |
| `compiler/lengthrange/accel<compiler-lengthrange-accel>` | *varies* |
| `compiler/lengthrange/maxforce<compiler-lengthrange-maxforce>` | *varies* |
| `compiler/lengthrange/timeconst<compiler-lengthrange-timeconst>` | $`T`$ |
| `compiler/lengthrange/timestep<compiler-lengthrange-timestep>` | $`T`$ |
| `compiler/lengthrange/inttotal<compiler-lengthrange-inttotal>` | $`T`$ |
| `compiler/lengthrange/interval<compiler-lengthrange-interval>` | $`T`$ |
| `compiler/lengthrange/tolrange<compiler-lengthrange-tolrange>` | $`1`$ |
| `option/timestep<option-timestep>` | $`T`$ |
| `option/impratio<option-impratio>` | $`1`$ |
| `option/tolerance<option-tolerance>` | $`1`$ |
| `option/ls_tolerance<option-ls_tolerance>` | $`1`$ |
| `option/noslip_tolerance<option-noslip_tolerance>` | $`1`$ |
| `option/ccd_tolerance<option-ccd_tolerance>` | $`L`$ |
| `option/sleep_tolerance<option-sleep_tolerance>` | $`L\,T^{-1}`$ |
| `option/gravity<option-gravity>` | $`L\,T^{-2}`$ |
| `option/wind<option-wind>` | $`L\,T^{-1}`$ |
| `option/magnetic<option-magnetic>` | *other* |
| `option/density<option-density>` | $`M\,L^{-3}`$ |
| `option/viscosity<option-viscosity>` | $`M\,L^{-1}\,T^{-1}`$ |
| `option/o_margin<option-o_margin>` | $`L`$ |
| `option/o_solref<option-o_solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `option/o_solimp<option-o_solimp>` | $`1,\ 1,\ L,\ 1,\ 1`$ |
| `option/o_friction<option-o_friction>` | $`1,\ 1,\ L,\ L,\ L`$ |
| `statistic/meaninertia<statistic-meaninertia>` | $`M\,L^{2}`$ |
| `statistic/meanmass<statistic-meanmass>` | $`M`$ |
| `statistic/meansize<statistic-meansize>` | $`L`$ |
| `statistic/extent<statistic-extent>` | $`L`$ |
| `statistic/center<statistic-center>` | $`L`$ |
| `visual/global/fovy<visual-global-fovy>` | $`A`$ |
| `visual/global/ipd<visual-global-ipd>` | $`L`$ |
| `visual/global/azimuth<visual-global-azimuth>` | $`A`$ |
| `visual/global/elevation<visual-global-elevation>` | $`A`$ |
| `visual/global/linewidth<visual-global-linewidth>` | $`1`$ |
| `visual/global/glow<visual-global-glow>` | $`1`$ |
| `visual/global/realtime<visual-global-realtime>` | $`1`$ |
| `visual/headlight/ambient<visual-headlight-ambient>` | $`1`$ |
| `visual/headlight/diffuse<visual-headlight-diffuse>` | $`1`$ |
| `visual/headlight/specular<visual-headlight-specular>` | $`1`$ |
| `visual/map/stiffness<visual-map-stiffness>` | $`T^{-2}`$ |
| `visual/map/stiffnessrot<visual-map-stiffnessrot>` | $`T^{-2}`$ |
| `visual/map/force<visual-map-force>` | $`T^{2}`$ |
| `visual/map/torque<visual-map-torque>` | $`L^{-1}\,T^{2}`$ |
| `visual/map/alpha<visual-map-alpha>` | $`1`$ |
| `visual/map/fogstart<visual-map-fogstart>` | $`1`$ |
| `visual/map/fogend<visual-map-fogend>` | $`1`$ |
| `visual/map/znear<visual-map-znear>` | $`1`$ |
| `visual/map/zfar<visual-map-zfar>` | $`1`$ |
| `visual/map/haze<visual-map-haze>` | $`1`$ |
| `visual/map/shadowclip<visual-map-shadowclip>` | $`1`$ |
| `visual/map/shadowscale<visual-map-shadowscale>` | $`1`$ |
| `visual/map/actuatortendon<visual-map-actuatortendon>` | $`1`$ |
| `visual/scale/forcewidth<visual-scale-forcewidth>` | $`1`$ |
| `visual/scale/contactwidth<visual-scale-contactwidth>` | $`1`$ |
| `visual/scale/contactheight<visual-scale-contactheight>` | $`1`$ |
| `visual/scale/connect<visual-scale-connect>` | $`1`$ |
| `visual/scale/com<visual-scale-com>` | $`1`$ |
| `visual/scale/camera<visual-scale-camera>` | $`1`$ |
| `visual/scale/light<visual-scale-light>` | $`1`$ |
| `visual/scale/selectpoint<visual-scale-selectpoint>` | $`1`$ |
| `visual/scale/jointlength<visual-scale-jointlength>` | $`1`$ |
| `visual/scale/jointwidth<visual-scale-jointwidth>` | $`1`$ |
| `visual/scale/actuatorlength<visual-scale-actuatorlength>` | $`1`$ |
| `visual/scale/actuatorwidth<visual-scale-actuatorwidth>` | $`1`$ |
| `visual/scale/framelength<visual-scale-framelength>` | $`1`$ |
| `visual/scale/framewidth<visual-scale-framewidth>` | $`1`$ |
| `visual/scale/constraint<visual-scale-constraint>` | $`1`$ |
| `visual/scale/slidercrank<visual-scale-slidercrank>` | $`1`$ |
| `visual/scale/frustum<visual-scale-frustum>` | $`1`$ |
| `visual/rgba/fog<visual-rgba-fog>` | $`1`$ |
| `visual/rgba/haze<visual-rgba-haze>` | $`1`$ |
| `visual/rgba/force<visual-rgba-force>` | $`1`$ |
| `visual/rgba/inertia<visual-rgba-inertia>` | $`1`$ |
| `visual/rgba/joint<visual-rgba-joint>` | $`1`$ |
| `visual/rgba/actuator<visual-rgba-actuator>` | $`1`$ |
| `visual/rgba/actuatornegative<visual-rgba-actuatornegative>` | $`1`$ |
| `visual/rgba/actuatorpositive<visual-rgba-actuatorpositive>` | $`1`$ |
| `visual/rgba/com<visual-rgba-com>` | $`1`$ |
| `visual/rgba/camera<visual-rgba-camera>` | $`1`$ |
| `visual/rgba/light<visual-rgba-light>` | $`1`$ |
| `visual/rgba/selectpoint<visual-rgba-selectpoint>` | $`1`$ |
| `visual/rgba/connect<visual-rgba-connect>` | $`1`$ |
| `visual/rgba/contactpoint<visual-rgba-contactpoint>` | $`1`$ |
| `visual/rgba/contactforce<visual-rgba-contactforce>` | $`1`$ |
| `visual/rgba/contactfriction<visual-rgba-contactfriction>` | $`1`$ |
| `visual/rgba/contacttorque<visual-rgba-contacttorque>` | $`1`$ |
| `visual/rgba/contactgap<visual-rgba-contactgap>` | $`1`$ |
| `visual/rgba/rangefinder<visual-rgba-rangefinder>` | $`1`$ |
| `visual/rgba/constraint<visual-rgba-constraint>` | $`1`$ |
| `visual/rgba/slidercrank<visual-rgba-slidercrank>` | $`1`$ |
| `visual/rgba/crankbroken<visual-rgba-crankbroken>` | $`1`$ |
| `visual/rgba/frustum<visual-rgba-frustum>` | $`1`$ |
| `visual/rgba/bv<visual-rgba-bv>` | $`1`$ |
| `visual/rgba/bvactive<visual-rgba-bvactive>` | $`1`$ |
| `asset/mesh/vertex<asset-mesh-vertex>` | $`1`$ |
| `asset/mesh/normal<asset-mesh-normal>` | $`1`$ |
| `asset/mesh/texcoord<asset-mesh-texcoord>` | $`1`$ |
| `asset/mesh/refpos<asset-mesh-refpos>` | $`1`$ |
| `asset/mesh/refquat<asset-mesh-refquat>` | $`1`$ |
| `asset/mesh/scale<asset-mesh-scale>` | $`L`$ |
| `asset/mesh/params<asset-mesh-params>` | *varies* |
| `asset/hfield/size<asset-hfield-size>` | $`L`$ |
| `asset/hfield/elevation<asset-hfield-elevation>` | $`1`$ |
| `asset/skin/rgba<asset-skin-rgba>` | $`1`$ |
| `asset/skin/inflate<asset-skin-inflate>` | $`L`$ |
| `asset/skin/vertex<asset-skin-vertex>` | $`L`$ |
| `asset/skin/texcoord<asset-skin-texcoord>` | $`1`$ |
| `skin/bone/bindpos<skin-bone-bindpos>` | $`L`$ |
| `skin/bone/bindquat<skin-bone-bindquat>` | $`1`$ |
| `skin/bone/vertweight<skin-bone-vertweight>` | $`1`$ |
| `asset/texture/rgb1<asset-texture-rgb1>` | $`1`$ |
| `asset/texture/rgb2<asset-texture-rgb2>` | $`1`$ |
| `asset/texture/markrgb<asset-texture-markrgb>` | $`1`$ |
| `asset/texture/random<asset-texture-random>` | $`1`$ |
| `asset/material/texrepeat<asset-material-texrepeat>` | *varies* |
| `asset/material/emission<asset-material-emission>` | $`1`$ |
| `asset/material/specular<asset-material-specular>` | $`1`$ |
| `asset/material/shininess<asset-material-shininess>` | $`1`$ |
| `asset/material/reflectance<asset-material-reflectance>` | $`1`$ |
| `asset/material/metallic<asset-material-metallic>` | $`1`$ |
| `asset/material/roughness<asset-material-roughness>` | $`1`$ |
| `asset/material/rgba<asset-material-rgba>` | $`1`$ |
| `body/pos<body-pos>` | $`L`$ |
| `body/quat<body-quat>` | $`1`$ |
| `body/axisangle<body-axisangle>` | $`1,\ 1,\ 1,\ A`$ |
| `body/xyaxes<body-xyaxes>` | $`1`$ |
| `body/zaxis<body-zaxis>` | $`1`$ |
| `body/euler<body-euler>` | $`A`$ |
| `body/gravcomp<body-gravcomp>` | $`1`$ |
| `body/user<body-user>` | *other* |
| `frame/pos<frame-pos>` | $`L`$ |
| `frame/quat<frame-quat>` | $`1`$ |
| `frame/axisangle<frame-axisangle>` | $`1,\ 1,\ 1,\ A`$ |
| `frame/xyaxes<frame-xyaxes>` | $`1`$ |
| `frame/zaxis<frame-zaxis>` | $`1`$ |
| `frame/euler<frame-euler>` | $`A`$ |
| `frame/scale<frame-scale>` | $`1`$ |
| `frame/massscale<frame-massscale>` | $`1`$ |
| `replicate/offset<replicate-offset>` | $`L`$ |
| `replicate/euler<replicate-euler>` | $`A`$ |
| `body/inertial/pos<body-inertial-pos>` | $`L`$ |
| `body/inertial/quat<body-inertial-quat>` | $`1`$ |
| `body/inertial/mass<body-inertial-mass>` | $`M`$ |
| `body/inertial/diaginertia<body-inertial-diaginertia>` | $`M\,L^{2}`$ |
| `body/inertial/axisangle<body-inertial-axisangle>` | $`1,\ 1,\ 1,\ A`$ |
| `body/inertial/xyaxes<body-inertial-xyaxes>` | $`1`$ |
| `body/inertial/zaxis<body-inertial-zaxis>` | $`1`$ |
| `body/inertial/euler<body-inertial-euler>` | $`A`$ |
| `body/inertial/fullinertia<body-inertial-fullinertia>` | $`M\,L^{2}`$ |
| `body/joint/pos<body-joint-pos>` | $`L`$ |
| `body/joint/axis<body-joint-axis>` | $`1`$ |
| `body/joint/springdamper<body-joint-springdamper>` | $`T,\ 1`$ |
| `body/joint/solreflimit<body-joint-solreflimit>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `body/joint/solimplimit<body-joint-solimplimit>` | $`1,\ 1,\ Q,\ 1,\ 1`$ |
| `body/joint/solreffriction<body-joint-solreffriction>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `body/joint/solimpfriction<body-joint-solimpfriction>` | $`1,\ 1,\ Q,\ 1,\ 1`$ |
| `body/joint/stiffness<body-joint-stiffness>` | $`F\,Q^{-1},\ F\,Q^{-2},\ F\,Q^{-3}`$ |
| `body/joint/range<body-joint-range>` | $`Q`$ |
| `body/joint/actuatorfrcrange<body-joint-actuatorfrcrange>` | $`F`$ |
| `body/joint/margin<body-joint-margin>` | $`Q`$ |
| `body/joint/ref<body-joint-ref>` | $`Q`$ |
| `body/joint/springref<body-joint-springref>` | $`Q`$ |
| `body/joint/springyield<body-joint-springyield>` | $`Q`$ |
| `body/joint/armature<body-joint-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `body/joint/damping<body-joint-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `body/joint/frictionloss<body-joint-frictionloss>` | $`F`$ |
| `body/joint/user<body-joint-user>` | *other* |
| `body/geom/size<body-geom-size>` | $`L`$ |
| `body/geom/friction<body-geom-friction>` | $`1,\ L,\ L`$ |
| `body/geom/mass<body-geom-mass>` | $`M`$ |
| `body/geom/density<body-geom-density>` | *varies* |
| `body/geom/solmix<body-geom-solmix>` | $`1`$ |
| `body/geom/solref<body-geom-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `body/geom/solimp<body-geom-solimp>` | $`1,\ 1,\ L,\ 1,\ 1`$ |
| `body/geom/margin<body-geom-margin>` | $`L`$ |
| `body/geom/gap<body-geom-gap>` | $`L`$ |
| `body/geom/surfacevel<body-geom-surfacevel>` | $`L\,T^{-1},\ L\,T^{-1},\ L\,T^{-1},\ A\,T^{-1},\ A\,T^{-1},\ A\,T^{-1}`$ |
| `body/geom/adhesion<body-geom-adhesion>` | $`M\,L\,T^{-2}`$ |
| `body/geom/fromto<body-geom-fromto>` | $`L`$ |
| `body/geom/pos<body-geom-pos>` | $`L`$ |
| `body/geom/quat<body-geom-quat>` | $`1`$ |
| `body/geom/axisangle<body-geom-axisangle>` | $`1,\ 1,\ 1,\ A`$ |
| `body/geom/xyaxes<body-geom-xyaxes>` | $`1`$ |
| `body/geom/zaxis<body-geom-zaxis>` | $`1`$ |
| `body/geom/euler<body-geom-euler>` | $`A`$ |
| `body/geom/fitscale<body-geom-fitscale>` | $`1`$ |
| `body/geom/rgba<body-geom-rgba>` | $`1`$ |
| `body/geom/fluidcoef<body-geom-fluidcoef>` | $`1`$ |
| `body/geom/user<body-geom-user>` | *other* |
| `body/site/pos<body-site-pos>` | $`L`$ |
| `body/site/quat<body-site-quat>` | $`1`$ |
| `body/site/axisangle<body-site-axisangle>` | $`1,\ 1,\ 1,\ A`$ |
| `body/site/xyaxes<body-site-xyaxes>` | $`1`$ |
| `body/site/zaxis<body-site-zaxis>` | $`1`$ |
| `body/site/euler<body-site-euler>` | $`A`$ |
| `body/site/size<body-site-size>` | $`L`$ |
| `body/site/fromto<body-site-fromto>` | $`L`$ |
| `body/site/rgba<body-site-rgba>` | $`1`$ |
| `body/site/user<body-site-user>` | *other* |
| `body/camera/fovy<body-camera-fovy>` | *varies* |
| `body/camera/ipd<body-camera-ipd>` | $`L`$ |
| `body/camera/pos<body-camera-pos>` | $`L`$ |
| `body/camera/quat<body-camera-quat>` | $`1`$ |
| `body/camera/axisangle<body-camera-axisangle>` | $`1,\ 1,\ 1,\ A`$ |
| `body/camera/xyaxes<body-camera-xyaxes>` | $`1`$ |
| `body/camera/zaxis<body-camera-zaxis>` | $`1`$ |
| `body/camera/euler<body-camera-euler>` | $`A`$ |
| `body/camera/focal<body-camera-focal>` | $`L`$ |
| `body/camera/focalpixel<body-camera-focalpixel>` | $`1`$ |
| `body/camera/principal<body-camera-principal>` | $`L`$ |
| `body/camera/principalpixel<body-camera-principalpixel>` | $`1`$ |
| `body/camera/sensorsize<body-camera-sensorsize>` | $`L`$ |
| `body/camera/user<body-camera-user>` | *other* |
| `body/light/pos<body-light-pos>` | $`L`$ |
| `body/light/dir<body-light-dir>` | $`1`$ |
| `body/light/bulbradius<body-light-bulbradius>` | $`L`$ |
| `body/light/intensity<body-light-intensity>` | *other* |
| `body/light/range<body-light-range>` | $`L`$ |
| `body/light/attenuation<body-light-attenuation>` | $`1,\ L^{-1},\ L^{-2}`$ |
| `body/light/cutoff<body-light-cutoff>` | $`A`$ |
| `body/light/softness<body-light-softness>` | $`1`$ |
| `body/light/exponent<body-light-exponent>` | $`1`$ |
| `body/light/ambient<body-light-ambient>` | $`1`$ |
| `body/light/diffuse<body-light-diffuse>` | $`1`$ |
| `body/light/specular<body-light-specular>` | $`1`$ |
| `body/flexcomp/spacing<body-flexcomp-spacing>` | $`L`$ |
| `body/flexcomp/radius<body-flexcomp-radius>` | $`L`$ |
| `body/flexcomp/mass<body-flexcomp-mass>` | $`M`$ |
| `body/flexcomp/inertiabox<body-flexcomp-inertiabox>` | $`L`$ |
| `body/flexcomp/scale<body-flexcomp-scale>` | $`L`$ |
| `body/flexcomp/point<body-flexcomp-point>` | $`1`$ |
| `body/flexcomp/element<body-flexcomp-element>` | $`1`$ |
| `body/flexcomp/texcoord<body-flexcomp-texcoord>` | $`1`$ |
| `body/flexcomp/rgba<body-flexcomp-rgba>` | $`1`$ |
| `body/flexcomp/pos<body-flexcomp-pos>` | $`L`$ |
| `body/flexcomp/quat<body-flexcomp-quat>` | $`1`$ |
| `body/flexcomp/axisangle<body-flexcomp-axisangle>` | $`1,\ 1,\ 1,\ A`$ |
| `body/flexcomp/xyaxes<body-flexcomp-xyaxes>` | $`1`$ |
| `body/flexcomp/zaxis<body-flexcomp-zaxis>` | $`1`$ |
| `body/flexcomp/euler<body-flexcomp-euler>` | $`A`$ |
| `body/flexcomp/origin<body-flexcomp-origin>` | $`1`$ |
| `flexcomp/edge/solref<flexcomp-edge-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `flexcomp/edge/solimp<flexcomp-edge-solimp>` | $`1,\ 1,\ L,\ 1,\ 1`$ |
| `flexcomp/edge/stiffness<flexcomp-edge-stiffness>` | $`M\,T^{-2}`$ |
| `flexcomp/edge/damping<flexcomp-edge-damping>` | $`M\,T^{-1}`$ |
| `flexcomp/elasticity/young<flexcomp-elasticity-young>` | $`M\,L^{-1}\,T^{-2}`$ |
| `flexcomp/elasticity/poisson<flexcomp-elasticity-poisson>` | $`1`$ |
| `flexcomp/elasticity/shear<flexcomp-elasticity-shear>` | $`M\,L^{-1}\,T^{-2}`$ |
| `flexcomp/elasticity/damping<flexcomp-elasticity-damping>` | $`T`$ |
| `flexcomp/elasticity/thickness<flexcomp-elasticity-thickness>` | $`L`$ |
| `flexcomp/elasticity/yield<flexcomp-elasticity-yield>` | $`1`$ |
| `flexcomp/elasticity/sectionsize<flexcomp-elasticity-sectionsize>` | $`L`$ |
| `flexcomp/contact/friction<flexcomp-contact-friction>` | $`1,\ L,\ L`$ |
| `flexcomp/contact/solmix<flexcomp-contact-solmix>` | $`1`$ |
| `flexcomp/contact/solref<flexcomp-contact-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `flexcomp/contact/solimp<flexcomp-contact-solimp>` | $`1,\ 1,\ L,\ 1,\ 1`$ |
| `flexcomp/contact/margin<flexcomp-contact-margin>` | $`L`$ |
| `flexcomp/contact/gap<flexcomp-contact-gap>` | $`L`$ |
| `flexcomp/pin/id<flexcomp-pin-id>` | $`1`$ |
| `flexcomp/pin/range<flexcomp-pin-range>` | $`1`$ |
| `flexcomp/pin/grid<flexcomp-pin-grid>` | $`1`$ |
| `flexcomp/pin/gridrange<flexcomp-pin-gridrange>` | $`1`$ |
| `deformable/flex/radius<deformable-flex-radius>` | $`L`$ |
| `deformable/flex/rgba<deformable-flex-rgba>` | $`1`$ |
| `deformable/flex/vertex<deformable-flex-vertex>` | $`L`$ |
| `deformable/flex/texcoord<deformable-flex-texcoord>` | $`1`$ |
| `deformable/flex/nodecoord<deformable-flex-nodecoord>` | $`L`$ |
| `flex/edge/stiffness<flex-edge-stiffness>` | $`M\,T^{-2}`$ |
| `flex/edge/damping<flex-edge-damping>` | $`M\,T^{-1}`$ |
| `contact/pair/friction<contact-pair-friction>` | $`1,\ 1,\ L,\ L,\ L`$ |
| `contact/pair/solref<contact-pair-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `contact/pair/solreffriction<contact-pair-solreffriction>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `contact/pair/solimp<contact-pair-solimp>` | $`1,\ 1,\ L,\ 1,\ 1`$ |
| `contact/pair/gap<contact-pair-gap>` | $`L`$ |
| `contact/pair/margin<contact-pair-margin>` | $`L`$ |
| `contact/pair/adhesion<contact-pair-adhesion>` | $`M\,L\,T^{-2}`$ |
| `tendon/spatial/range<tendon-spatial-range>` | $`Q`$ |
| `tendon/spatial/actuatorfrcrange<tendon-spatial-actuatorfrcrange>` | $`F`$ |
| `tendon/spatial/solreflimit<tendon-spatial-solreflimit>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `tendon/spatial/solimplimit<tendon-spatial-solimplimit>` | $`1,\ 1,\ Q,\ 1,\ 1`$ |
| `tendon/spatial/solreffriction<tendon-spatial-solreffriction>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `tendon/spatial/solimpfriction<tendon-spatial-solimpfriction>` | $`1,\ 1,\ Q,\ 1,\ 1`$ |
| `tendon/spatial/frictionloss<tendon-spatial-frictionloss>` | $`F`$ |
| `tendon/spatial/springlength<tendon-spatial-springlength>` | $`Q`$ |
| `tendon/spatial/springyield<tendon-spatial-springyield>` | $`Q`$ |
| `tendon/spatial/width<tendon-spatial-width>` | $`L`$ |
| `tendon/spatial/margin<tendon-spatial-margin>` | $`Q`$ |
| `tendon/spatial/stiffness<tendon-spatial-stiffness>` | $`F\,Q^{-1},\ F\,Q^{-2},\ F\,Q^{-3}`$ |
| `tendon/spatial/damping<tendon-spatial-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `tendon/spatial/armature<tendon-spatial-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `tendon/spatial/rgba<tendon-spatial-rgba>` | $`1`$ |
| `tendon/spatial/user<tendon-spatial-user>` | *other* |
| `spatial/pulley/divisor<spatial-pulley-divisor>` | $`1`$ |
| `tendon/fixed/range<tendon-fixed-range>` | $`Q`$ |
| `tendon/fixed/actuatorfrcrange<tendon-fixed-actuatorfrcrange>` | $`F`$ |
| `tendon/fixed/solreflimit<tendon-fixed-solreflimit>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `tendon/fixed/solimplimit<tendon-fixed-solimplimit>` | $`1,\ 1,\ Q,\ 1,\ 1`$ |
| `tendon/fixed/solreffriction<tendon-fixed-solreffriction>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `tendon/fixed/solimpfriction<tendon-fixed-solimpfriction>` | $`1,\ 1,\ Q,\ 1,\ 1`$ |
| `tendon/fixed/frictionloss<tendon-fixed-frictionloss>` | $`F`$ |
| `tendon/fixed/springlength<tendon-fixed-springlength>` | $`Q`$ |
| `tendon/fixed/springyield<tendon-fixed-springyield>` | $`Q`$ |
| `tendon/fixed/margin<tendon-fixed-margin>` | $`Q`$ |
| `tendon/fixed/stiffness<tendon-fixed-stiffness>` | $`F\,Q^{-1},\ F\,Q^{-2},\ F\,Q^{-3}`$ |
| `tendon/fixed/damping<tendon-fixed-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `tendon/fixed/armature<tendon-fixed-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `tendon/fixed/user<tendon-fixed-user>` | *other* |
| `fixed/joint/coef<fixed-joint-coef>` | *varies* |
| `equality/connect/solref<equality-connect-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `equality/connect/solimp<equality-connect-solimp>` | *varies* |
| `equality/connect/anchor<equality-connect-anchor>` | $`L`$ |
| `equality/weld/solref<equality-weld-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `equality/weld/solimp<equality-weld-solimp>` | *varies* |
| `equality/weld/relpose<equality-weld-relpose>` | $`L,\ L,\ L,\ 1,\ 1,\ 1,\ 1`$ |
| `equality/weld/anchor<equality-weld-anchor>` | $`L`$ |
| `equality/weld/torquescale<equality-weld-torquescale>` | $`L`$ |
| `equality/joint/solref<equality-joint-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `equality/joint/solimp<equality-joint-solimp>` | *varies* |
| `equality/joint/polycoef<equality-joint-polycoef>` | *varies* |
| `equality/tendon/solref<equality-tendon-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `equality/tendon/solimp<equality-tendon-solimp>` | *varies* |
| `equality/tendon/polycoef<equality-tendon-polycoef>` | *varies* |
| `equality/flex/solref<equality-flex-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `equality/flex/solimp<equality-flex-solimp>` | *varies* |
| `equality/flexstrain/solref<equality-flexstrain-solref>` | $`T,\ 1`$ or $`T^{-2},\ T^{-1}`$ |
| `equality/flexstrain/solimp<equality-flexstrain-solimp>` | *varies* |
| `equality/flexstrain/cell<equality-flexstrain-cell>` | $`1`$ |
| `actuator/general/delay<actuator-general-delay>` | $`T`$ |
| `actuator/general/ctrlrange<actuator-general-ctrlrange>` | *varies* |
| `actuator/general/user<actuator-general-user>` | *other* |
| `actuator/general/forcerange<actuator-general-forcerange>` | $`F`$ |
| `actuator/general/actrange<actuator-general-actrange>` | *varies* |
| `actuator/general/lengthrange<actuator-general-lengthrange>` | $`Q`$ |
| `actuator/general/gear<actuator-general-gear>` | *varies* |
| `actuator/general/damping<actuator-general-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/general/armature<actuator-general-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/general/cranklength<actuator-general-cranklength>` | $`L`$ |
| `actuator/general/velrange<actuator-general-velrange>` | $`Q\,T^{-1}`$ |
| `actuator/general/ffrange<actuator-general-ffrange>` | $`F`$ |
| `actuator/general/inheritrange<actuator-general-inheritrange>` | $`1`$ |
| `actuator/general/dynprm<actuator-general-dynprm>` | *varies* |
| `actuator/general/gainprm<actuator-general-gainprm>` | *varies* |
| `actuator/general/biasprm<actuator-general-biasprm>` | *varies* |
| `actuator/motor/delay<actuator-motor-delay>` | $`T`$ |
| `actuator/motor/ctrlrange<actuator-motor-ctrlrange>` | $`1`$ |
| `actuator/motor/user<actuator-motor-user>` | *other* |
| `actuator/motor/forcerange<actuator-motor-forcerange>` | $`F`$ |
| `actuator/motor/lengthrange<actuator-motor-lengthrange>` | $`Q`$ |
| `actuator/motor/gear<actuator-motor-gear>` | *varies* |
| `actuator/motor/damping<actuator-motor-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/motor/armature<actuator-motor-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/motor/cranklength<actuator-motor-cranklength>` | $`L`$ |
| `actuator/position/delay<actuator-position-delay>` | $`T`$ |
| `actuator/position/ctrlrange<actuator-position-ctrlrange>` | $`Q`$ |
| `actuator/position/user<actuator-position-user>` | *other* |
| `actuator/position/inheritrange<actuator-position-inheritrange>` | $`1`$ |
| `actuator/position/forcerange<actuator-position-forcerange>` | $`F`$ |
| `actuator/position/lengthrange<actuator-position-lengthrange>` | $`Q`$ |
| `actuator/position/gear<actuator-position-gear>` | *varies* |
| `actuator/position/damping<actuator-position-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/position/armature<actuator-position-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/position/cranklength<actuator-position-cranklength>` | $`L`$ |
| `actuator/position/kp<actuator-position-kp>` | $`F\,Q^{-1}`$ |
| `actuator/position/kv<actuator-position-kv>` | $`F\,T\,Q^{-1}`$ |
| `actuator/position/dampratio<actuator-position-dampratio>` | $`1`$ |
| `actuator/position/timeconst<actuator-position-timeconst>` | $`T`$ |
| `actuator/velocity/delay<actuator-velocity-delay>` | $`T`$ |
| `actuator/velocity/ctrlrange<actuator-velocity-ctrlrange>` | $`Q\,T^{-1}`$ |
| `actuator/velocity/user<actuator-velocity-user>` | *other* |
| `actuator/velocity/forcerange<actuator-velocity-forcerange>` | $`F`$ |
| `actuator/velocity/lengthrange<actuator-velocity-lengthrange>` | $`Q`$ |
| `actuator/velocity/gear<actuator-velocity-gear>` | *varies* |
| `actuator/velocity/damping<actuator-velocity-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/velocity/armature<actuator-velocity-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/velocity/cranklength<actuator-velocity-cranklength>` | $`L`$ |
| `actuator/velocity/kv<actuator-velocity-kv>` | $`F\,T\,Q^{-1}`$ |
| `actuator/intvelocity/delay<actuator-intvelocity-delay>` | $`T`$ |
| `actuator/intvelocity/ctrlrange<actuator-intvelocity-ctrlrange>` | $`Q\,T^{-1}`$ |
| `actuator/intvelocity/user<actuator-intvelocity-user>` | *other* |
| `actuator/intvelocity/forcerange<actuator-intvelocity-forcerange>` | $`F`$ |
| `actuator/intvelocity/actrange<actuator-intvelocity-actrange>` | $`Q`$ |
| `actuator/intvelocity/inheritrange<actuator-intvelocity-inheritrange>` | $`1`$ |
| `actuator/intvelocity/lengthrange<actuator-intvelocity-lengthrange>` | $`Q`$ |
| `actuator/intvelocity/gear<actuator-intvelocity-gear>` | *varies* |
| `actuator/intvelocity/damping<actuator-intvelocity-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/intvelocity/armature<actuator-intvelocity-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/intvelocity/cranklength<actuator-intvelocity-cranklength>` | $`L`$ |
| `actuator/intvelocity/kp<actuator-intvelocity-kp>` | $`F\,Q^{-1}`$ |
| `actuator/intvelocity/kv<actuator-intvelocity-kv>` | $`F\,T\,Q^{-1}`$ |
| `actuator/intvelocity/dampratio<actuator-intvelocity-dampratio>` | $`1`$ |
| `actuator/orientation/delay<actuator-orientation-delay>` | $`T`$ |
| `actuator/orientation/ctrlrange<actuator-orientation-ctrlrange>` | *varies* |
| `actuator/orientation/user<actuator-orientation-user>` | *other* |
| `actuator/orientation/forcerange<actuator-orientation-forcerange>` | $`F`$ |
| `actuator/orientation/kp<actuator-orientation-kp>` | $`F\,Q^{-1}`$ |
| `actuator/orientation/kv<actuator-orientation-kv>` | $`F\,T\,Q^{-1}`$ |
| `actuator/orientation/dampratio<actuator-orientation-dampratio>` | $`1`$ |
| `actuator/pid/delay<actuator-pid-delay>` | $`T`$ |
| `actuator/pid/ctrlrange<actuator-pid-ctrlrange>` | *varies* |
| `actuator/pid/user<actuator-pid-user>` | *other* |
| `actuator/pid/posrange<actuator-pid-posrange>` | $`Q`$ |
| `actuator/pid/velrange<actuator-pid-velrange>` | $`Q\,T^{-1}`$ |
| `actuator/pid/ffrange<actuator-pid-ffrange>` | $`F`$ |
| `actuator/pid/forcerange<actuator-pid-forcerange>` | $`F`$ |
| `actuator/pid/inheritrange<actuator-pid-inheritrange>` | $`1`$ |
| `actuator/pid/lengthrange<actuator-pid-lengthrange>` | $`Q`$ |
| `actuator/pid/gear<actuator-pid-gear>` | *varies* |
| `actuator/pid/damping<actuator-pid-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/pid/armature<actuator-pid-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/pid/cranklength<actuator-pid-cranklength>` | $`L`$ |
| `actuator/pid/kp<actuator-pid-kp>` | $`F\,Q^{-1}`$ |
| `actuator/pid/kv<actuator-pid-kv>` | $`F\,T\,Q^{-1}`$ |
| `actuator/pid/dampratio<actuator-pid-dampratio>` | $`1`$ |
| `actuator/pid/ki<actuator-pid-ki>` | $`F\,Q^{-1}\,T^{-1}`$ |
| `actuator/pid/imax<actuator-pid-imax>` | $`Q\,T`$ |
| `actuator/pid/slewmax<actuator-pid-slewmax>` | $`Q\,T^{-1}`$ |
| `actuator/damper/delay<actuator-damper-delay>` | $`T`$ |
| `actuator/damper/ctrlrange<actuator-damper-ctrlrange>` | $`1`$ |
| `actuator/damper/user<actuator-damper-user>` | *other* |
| `actuator/damper/forcerange<actuator-damper-forcerange>` | $`F`$ |
| `actuator/damper/lengthrange<actuator-damper-lengthrange>` | $`Q`$ |
| `actuator/damper/gear<actuator-damper-gear>` | *varies* |
| `actuator/damper/damping<actuator-damper-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/damper/armature<actuator-damper-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/damper/cranklength<actuator-damper-cranklength>` | $`L`$ |
| `actuator/damper/kv<actuator-damper-kv>` | $`F\,T\,Q^{-1}`$ |
| `actuator/cylinder/delay<actuator-cylinder-delay>` | $`T`$ |
| `actuator/cylinder/ctrlrange<actuator-cylinder-ctrlrange>` | $`F\,L^{-2}`$ |
| `actuator/cylinder/user<actuator-cylinder-user>` | *other* |
| `actuator/cylinder/forcerange<actuator-cylinder-forcerange>` | $`F`$ |
| `actuator/cylinder/lengthrange<actuator-cylinder-lengthrange>` | $`Q`$ |
| `actuator/cylinder/gear<actuator-cylinder-gear>` | *varies* |
| `actuator/cylinder/damping<actuator-cylinder-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/cylinder/armature<actuator-cylinder-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/cylinder/cranklength<actuator-cylinder-cranklength>` | $`L`$ |
| `actuator/cylinder/timeconst<actuator-cylinder-timeconst>` | $`T`$ |
| `actuator/cylinder/area<actuator-cylinder-area>` | $`L^{2}`$ |
| `actuator/cylinder/diameter<actuator-cylinder-diameter>` | $`L`$ |
| `actuator/cylinder/bias<actuator-cylinder-bias>` | $`F,\ F\,Q^{-1},\ F\,T\,Q^{-1}`$ |
| `actuator/muscle/delay<actuator-muscle-delay>` | $`T`$ |
| `actuator/muscle/ctrlrange<actuator-muscle-ctrlrange>` | $`1`$ |
| `actuator/muscle/user<actuator-muscle-user>` | *other* |
| `actuator/muscle/forcerange<actuator-muscle-forcerange>` | $`F`$ |
| `actuator/muscle/lengthrange<actuator-muscle-lengthrange>` | $`Q`$ |
| `actuator/muscle/gear<actuator-muscle-gear>` | *varies* |
| `actuator/muscle/damping<actuator-muscle-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/muscle/armature<actuator-muscle-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/muscle/cranklength<actuator-muscle-cranklength>` | $`L`$ |
| `actuator/muscle/timeconst<actuator-muscle-timeconst>` | $`T`$ |
| `actuator/muscle/tausmooth<actuator-muscle-tausmooth>` | $`1`$ |
| `actuator/muscle/range<actuator-muscle-range>` | $`1`$ |
| `actuator/muscle/force<actuator-muscle-force>` | $`F`$ |
| `actuator/muscle/scale<actuator-muscle-scale>` | *varies* |
| `actuator/muscle/lmin<actuator-muscle-lmin>` | $`1`$ |
| `actuator/muscle/lmax<actuator-muscle-lmax>` | $`1`$ |
| `actuator/muscle/vmax<actuator-muscle-vmax>` | $`T^{-1}`$ |
| `actuator/muscle/fpmax<actuator-muscle-fpmax>` | $`1`$ |
| `actuator/muscle/fvmax<actuator-muscle-fvmax>` | $`1`$ |
| `actuator/adhesion/delay<actuator-adhesion-delay>` | $`T`$ |
| `actuator/adhesion/ctrlrange<actuator-adhesion-ctrlrange>` | $`1`$ |
| `actuator/adhesion/user<actuator-adhesion-user>` | *other* |
| `actuator/adhesion/forcerange<actuator-adhesion-forcerange>` | $`M\,L\,T^{-2}`$ |
| `actuator/adhesion/gain<actuator-adhesion-gain>` | $`M\,L\,T^{-2}`$ |
| `actuator/dcmotor/delay<actuator-dcmotor-delay>` | $`T`$ |
| `actuator/dcmotor/ctrlrange<actuator-dcmotor-ctrlrange>` | *varies* |
| `actuator/dcmotor/user<actuator-dcmotor-user>` | *other* |
| `actuator/dcmotor/lengthrange<actuator-dcmotor-lengthrange>` | $`Q`$ |
| `actuator/dcmotor/gear<actuator-dcmotor-gear>` | *varies* |
| `actuator/dcmotor/damping<actuator-dcmotor-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/dcmotor/armature<actuator-dcmotor-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/dcmotor/cranklength<actuator-dcmotor-cranklength>` | $`L`$ |
| `actuator/dcmotor/motorconst<actuator-dcmotor-motorconst>` | *other* |
| `actuator/dcmotor/resistance<actuator-dcmotor-resistance>` | *other* |
| `actuator/dcmotor/nominal<actuator-dcmotor-nominal>` | *other* |
| `actuator/dcmotor/saturation<actuator-dcmotor-saturation>` | *other* |
| `actuator/dcmotor/inductance<actuator-dcmotor-inductance>` | *other* |
| `actuator/dcmotor/cogging<actuator-dcmotor-cogging>` | $`F,\ 1,\ A`$ |
| `actuator/dcmotor/controller<actuator-dcmotor-controller>` | *other* |
| `actuator/dcmotor/thermal<actuator-dcmotor-thermal>` | *other* |
| `actuator/dcmotor/lugre<actuator-dcmotor-lugre>` | $`F\,Q^{-1},\ F\,T\,Q^{-1},\ F,\ F,\ Q\,T^{-1}`$ |
| `actuator/plugin/delay<actuator-plugin-delay>` | $`T`$ |
| `actuator/plugin/ctrlrange<actuator-plugin-ctrlrange>` | *other* |
| `actuator/plugin/user<actuator-plugin-user>` | *other* |
| `actuator/plugin/forcerange<actuator-plugin-forcerange>` | $`F`$ |
| `actuator/plugin/actrange<actuator-plugin-actrange>` | *other* |
| `actuator/plugin/lengthrange<actuator-plugin-lengthrange>` | $`Q`$ |
| `actuator/plugin/gear<actuator-plugin-gear>` | *varies* |
| `actuator/plugin/damping<actuator-plugin-damping>` | $`F\,T\,Q^{-1},\ F\,T^{2}\,Q^{-2},\ F\,T^{3}\,Q^{-3}`$ |
| `actuator/plugin/armature<actuator-plugin-armature>` | $`F\,T^{2}\,Q^{-1}`$ |
| `actuator/plugin/cranklength<actuator-plugin-cranklength>` | $`L`$ |
| `actuator/plugin/dynprm<actuator-plugin-dynprm>` | *other* |
| `sensor/touch/delay<sensor-touch-delay>` | $`T`$ |
| `sensor/touch/interval<sensor-touch-interval>` | $`T`$ |
| `sensor/touch/cutoff<sensor-touch-cutoff>` | $`M\,L\,T^{-2}`$ |
| `sensor/touch/noise<sensor-touch-noise>` | $`M\,L\,T^{-2}`$ |
| `sensor/touch/user<sensor-touch-user>` | *other* |
| `sensor/accelerometer/delay<sensor-accelerometer-delay>` | $`T`$ |
| `sensor/accelerometer/interval<sensor-accelerometer-interval>` | $`T`$ |
| `sensor/accelerometer/cutoff<sensor-accelerometer-cutoff>` | $`L\,T^{-2}`$ |
| `sensor/accelerometer/noise<sensor-accelerometer-noise>` | $`L\,T^{-2}`$ |
| `sensor/accelerometer/user<sensor-accelerometer-user>` | *other* |
| `sensor/velocimeter/delay<sensor-velocimeter-delay>` | $`T`$ |
| `sensor/velocimeter/interval<sensor-velocimeter-interval>` | $`T`$ |
| `sensor/velocimeter/cutoff<sensor-velocimeter-cutoff>` | $`L\,T^{-1}`$ |
| `sensor/velocimeter/noise<sensor-velocimeter-noise>` | $`L\,T^{-1}`$ |
| `sensor/velocimeter/user<sensor-velocimeter-user>` | *other* |
| `sensor/gyro/delay<sensor-gyro-delay>` | $`T`$ |
| `sensor/gyro/interval<sensor-gyro-interval>` | $`T`$ |
| `sensor/gyro/cutoff<sensor-gyro-cutoff>` | $`A\,T^{-1}`$ |
| `sensor/gyro/noise<sensor-gyro-noise>` | $`A\,T^{-1}`$ |
| `sensor/gyro/user<sensor-gyro-user>` | *other* |
| `sensor/force/delay<sensor-force-delay>` | $`T`$ |
| `sensor/force/interval<sensor-force-interval>` | $`T`$ |
| `sensor/force/cutoff<sensor-force-cutoff>` | $`M\,L\,T^{-2}`$ |
| `sensor/force/noise<sensor-force-noise>` | $`M\,L\,T^{-2}`$ |
| `sensor/force/user<sensor-force-user>` | *other* |
| `sensor/torque/delay<sensor-torque-delay>` | $`T`$ |
| `sensor/torque/interval<sensor-torque-interval>` | $`T`$ |
| `sensor/torque/cutoff<sensor-torque-cutoff>` | $`M\,L^{2}\,T^{-2}`$ |
| `sensor/torque/noise<sensor-torque-noise>` | $`M\,L^{2}\,T^{-2}`$ |
| `sensor/torque/user<sensor-torque-user>` | *other* |
| `sensor/magnetometer/delay<sensor-magnetometer-delay>` | $`T`$ |
| `sensor/magnetometer/interval<sensor-magnetometer-interval>` | $`T`$ |
| `sensor/magnetometer/cutoff<sensor-magnetometer-cutoff>` | *other* |
| `sensor/magnetometer/noise<sensor-magnetometer-noise>` | *other* |
| `sensor/magnetometer/user<sensor-magnetometer-user>` | *other* |
| `sensor/camprojection/delay<sensor-camprojection-delay>` | $`T`$ |
| `sensor/camprojection/interval<sensor-camprojection-interval>` | $`T`$ |
| `sensor/camprojection/cutoff<sensor-camprojection-cutoff>` | $`1`$ |
| `sensor/camprojection/noise<sensor-camprojection-noise>` | $`1`$ |
| `sensor/camprojection/user<sensor-camprojection-user>` | *other* |
| `sensor/rangefinder/delay<sensor-rangefinder-delay>` | $`T`$ |
| `sensor/rangefinder/interval<sensor-rangefinder-interval>` | $`T`$ |
| `sensor/rangefinder/cutoff<sensor-rangefinder-cutoff>` | *varies* |
| `sensor/rangefinder/noise<sensor-rangefinder-noise>` | *varies* |
| `sensor/rangefinder/user<sensor-rangefinder-user>` | *other* |
| `sensor/jointpos/delay<sensor-jointpos-delay>` | $`T`$ |
| `sensor/jointpos/interval<sensor-jointpos-interval>` | $`T`$ |
| `sensor/jointpos/cutoff<sensor-jointpos-cutoff>` | $`Q`$ |
| `sensor/jointpos/noise<sensor-jointpos-noise>` | $`Q`$ |
| `sensor/jointpos/user<sensor-jointpos-user>` | *other* |
| `sensor/jointvel/delay<sensor-jointvel-delay>` | $`T`$ |
| `sensor/jointvel/interval<sensor-jointvel-interval>` | $`T`$ |
| `sensor/jointvel/cutoff<sensor-jointvel-cutoff>` | $`Q\,T^{-1}`$ |
| `sensor/jointvel/noise<sensor-jointvel-noise>` | $`Q\,T^{-1}`$ |
| `sensor/jointvel/user<sensor-jointvel-user>` | *other* |
| `sensor/tendonpos/delay<sensor-tendonpos-delay>` | $`T`$ |
| `sensor/tendonpos/interval<sensor-tendonpos-interval>` | $`T`$ |
| `sensor/tendonpos/cutoff<sensor-tendonpos-cutoff>` | $`Q`$ |
| `sensor/tendonpos/noise<sensor-tendonpos-noise>` | $`Q`$ |
| `sensor/tendonpos/user<sensor-tendonpos-user>` | *other* |
| `sensor/tendonvel/delay<sensor-tendonvel-delay>` | $`T`$ |
| `sensor/tendonvel/interval<sensor-tendonvel-interval>` | $`T`$ |
| `sensor/tendonvel/cutoff<sensor-tendonvel-cutoff>` | $`Q\,T^{-1}`$ |
| `sensor/tendonvel/noise<sensor-tendonvel-noise>` | $`Q\,T^{-1}`$ |
| `sensor/tendonvel/user<sensor-tendonvel-user>` | *other* |
| `sensor/actuatorpos/delay<sensor-actuatorpos-delay>` | $`T`$ |
| `sensor/actuatorpos/interval<sensor-actuatorpos-interval>` | $`T`$ |
| `sensor/actuatorpos/cutoff<sensor-actuatorpos-cutoff>` | $`Q`$ |
| `sensor/actuatorpos/noise<sensor-actuatorpos-noise>` | $`Q`$ |
| `sensor/actuatorpos/user<sensor-actuatorpos-user>` | *other* |
| `sensor/actuatorvel/delay<sensor-actuatorvel-delay>` | $`T`$ |
| `sensor/actuatorvel/interval<sensor-actuatorvel-interval>` | $`T`$ |
| `sensor/actuatorvel/cutoff<sensor-actuatorvel-cutoff>` | $`Q\,T^{-1}`$ |
| `sensor/actuatorvel/noise<sensor-actuatorvel-noise>` | $`Q\,T^{-1}`$ |
| `sensor/actuatorvel/user<sensor-actuatorvel-user>` | *other* |
| `sensor/actuatorfrc/delay<sensor-actuatorfrc-delay>` | $`T`$ |
| `sensor/actuatorfrc/interval<sensor-actuatorfrc-interval>` | $`T`$ |
| `sensor/actuatorfrc/cutoff<sensor-actuatorfrc-cutoff>` | $`F`$ |
| `sensor/actuatorfrc/noise<sensor-actuatorfrc-noise>` | $`F`$ |
| `sensor/actuatorfrc/user<sensor-actuatorfrc-user>` | *other* |
| `sensor/jointactuatorfrc/delay<sensor-jointactuatorfrc-delay>` | $`T`$ |
| `sensor/jointactuatorfrc/interval<sensor-jointactuatorfrc-interval>` | $`T`$ |
| `sensor/jointactuatorfrc/cutoff<sensor-jointactuatorfrc-cutoff>` | $`F`$ |
| `sensor/jointactuatorfrc/noise<sensor-jointactuatorfrc-noise>` | $`F`$ |
| `sensor/jointactuatorfrc/user<sensor-jointactuatorfrc-user>` | *other* |
| `sensor/tendonactuatorfrc/delay<sensor-tendonactuatorfrc-delay>` | $`T`$ |
| `sensor/tendonactuatorfrc/interval<sensor-tendonactuatorfrc-interval>` | $`T`$ |
| `sensor/tendonactuatorfrc/cutoff<sensor-tendonactuatorfrc-cutoff>` | $`F`$ |
| `sensor/tendonactuatorfrc/noise<sensor-tendonactuatorfrc-noise>` | $`F`$ |
| `sensor/tendonactuatorfrc/user<sensor-tendonactuatorfrc-user>` | *other* |
| `sensor/ballquat/delay<sensor-ballquat-delay>` | $`T`$ |
| `sensor/ballquat/interval<sensor-ballquat-interval>` | $`T`$ |
| `sensor/ballquat/cutoff<sensor-ballquat-cutoff>` | $`1`$ |
| `sensor/ballquat/noise<sensor-ballquat-noise>` | $`1`$ |
| `sensor/ballquat/user<sensor-ballquat-user>` | *other* |
| `sensor/ballangvel/delay<sensor-ballangvel-delay>` | $`T`$ |
| `sensor/ballangvel/interval<sensor-ballangvel-interval>` | $`T`$ |
| `sensor/ballangvel/cutoff<sensor-ballangvel-cutoff>` | $`A\,T^{-1}`$ |
| `sensor/ballangvel/noise<sensor-ballangvel-noise>` | $`A\,T^{-1}`$ |
| `sensor/ballangvel/user<sensor-ballangvel-user>` | *other* |
| `sensor/jointlimitpos/delay<sensor-jointlimitpos-delay>` | $`T`$ |
| `sensor/jointlimitpos/interval<sensor-jointlimitpos-interval>` | $`T`$ |
| `sensor/jointlimitpos/cutoff<sensor-jointlimitpos-cutoff>` | $`Q`$ |
| `sensor/jointlimitpos/noise<sensor-jointlimitpos-noise>` | $`Q`$ |
| `sensor/jointlimitpos/user<sensor-jointlimitpos-user>` | *other* |
| `sensor/jointlimitvel/delay<sensor-jointlimitvel-delay>` | $`T`$ |
| `sensor/jointlimitvel/interval<sensor-jointlimitvel-interval>` | $`T`$ |
| `sensor/jointlimitvel/cutoff<sensor-jointlimitvel-cutoff>` | $`Q\,T^{-1}`$ |
| `sensor/jointlimitvel/noise<sensor-jointlimitvel-noise>` | $`Q\,T^{-1}`$ |
| `sensor/jointlimitvel/user<sensor-jointlimitvel-user>` | *other* |
| `sensor/jointlimitfrc/delay<sensor-jointlimitfrc-delay>` | $`T`$ |
| `sensor/jointlimitfrc/interval<sensor-jointlimitfrc-interval>` | $`T`$ |
| `sensor/jointlimitfrc/cutoff<sensor-jointlimitfrc-cutoff>` | $`F`$ |
| `sensor/jointlimitfrc/noise<sensor-jointlimitfrc-noise>` | $`F`$ |
| `sensor/jointlimitfrc/user<sensor-jointlimitfrc-user>` | *other* |
| `sensor/tendonlimitpos/delay<sensor-tendonlimitpos-delay>` | $`T`$ |
| `sensor/tendonlimitpos/interval<sensor-tendonlimitpos-interval>` | $`T`$ |
| `sensor/tendonlimitpos/cutoff<sensor-tendonlimitpos-cutoff>` | $`Q`$ |
| `sensor/tendonlimitpos/noise<sensor-tendonlimitpos-noise>` | $`Q`$ |
| `sensor/tendonlimitpos/user<sensor-tendonlimitpos-user>` | *other* |
| `sensor/tendonlimitvel/delay<sensor-tendonlimitvel-delay>` | $`T`$ |
| `sensor/tendonlimitvel/interval<sensor-tendonlimitvel-interval>` | $`T`$ |
| `sensor/tendonlimitvel/cutoff<sensor-tendonlimitvel-cutoff>` | $`Q\,T^{-1}`$ |
| `sensor/tendonlimitvel/noise<sensor-tendonlimitvel-noise>` | $`Q\,T^{-1}`$ |
| `sensor/tendonlimitvel/user<sensor-tendonlimitvel-user>` | *other* |
| `sensor/tendonlimitfrc/delay<sensor-tendonlimitfrc-delay>` | $`T`$ |
| `sensor/tendonlimitfrc/interval<sensor-tendonlimitfrc-interval>` | $`T`$ |
| `sensor/tendonlimitfrc/cutoff<sensor-tendonlimitfrc-cutoff>` | $`F`$ |
| `sensor/tendonlimitfrc/noise<sensor-tendonlimitfrc-noise>` | $`F`$ |
| `sensor/tendonlimitfrc/user<sensor-tendonlimitfrc-user>` | *other* |
| `sensor/framepos/delay<sensor-framepos-delay>` | $`T`$ |
| `sensor/framepos/interval<sensor-framepos-interval>` | $`T`$ |
| `sensor/framepos/cutoff<sensor-framepos-cutoff>` | $`L`$ |
| `sensor/framepos/noise<sensor-framepos-noise>` | $`L`$ |
| `sensor/framepos/user<sensor-framepos-user>` | *other* |
| `sensor/framequat/delay<sensor-framequat-delay>` | $`T`$ |
| `sensor/framequat/interval<sensor-framequat-interval>` | $`T`$ |
| `sensor/framequat/cutoff<sensor-framequat-cutoff>` | $`1`$ |
| `sensor/framequat/noise<sensor-framequat-noise>` | $`1`$ |
| `sensor/framequat/user<sensor-framequat-user>` | *other* |
| `sensor/framexaxis/delay<sensor-framexaxis-delay>` | $`T`$ |
| `sensor/framexaxis/interval<sensor-framexaxis-interval>` | $`T`$ |
| `sensor/framexaxis/cutoff<sensor-framexaxis-cutoff>` | $`1`$ |
| `sensor/framexaxis/noise<sensor-framexaxis-noise>` | $`1`$ |
| `sensor/framexaxis/user<sensor-framexaxis-user>` | *other* |
| `sensor/frameyaxis/delay<sensor-frameyaxis-delay>` | $`T`$ |
| `sensor/frameyaxis/interval<sensor-frameyaxis-interval>` | $`T`$ |
| `sensor/frameyaxis/cutoff<sensor-frameyaxis-cutoff>` | $`1`$ |
| `sensor/frameyaxis/noise<sensor-frameyaxis-noise>` | $`1`$ |
| `sensor/frameyaxis/user<sensor-frameyaxis-user>` | *other* |
| `sensor/framezaxis/delay<sensor-framezaxis-delay>` | $`T`$ |
| `sensor/framezaxis/interval<sensor-framezaxis-interval>` | $`T`$ |
| `sensor/framezaxis/cutoff<sensor-framezaxis-cutoff>` | $`1`$ |
| `sensor/framezaxis/noise<sensor-framezaxis-noise>` | $`1`$ |
| `sensor/framezaxis/user<sensor-framezaxis-user>` | *other* |
| `sensor/framelinvel/delay<sensor-framelinvel-delay>` | $`T`$ |
| `sensor/framelinvel/interval<sensor-framelinvel-interval>` | $`T`$ |
| `sensor/framelinvel/cutoff<sensor-framelinvel-cutoff>` | $`L\,T^{-1}`$ |
| `sensor/framelinvel/noise<sensor-framelinvel-noise>` | $`L\,T^{-1}`$ |
| `sensor/framelinvel/user<sensor-framelinvel-user>` | *other* |
| `sensor/frameangvel/delay<sensor-frameangvel-delay>` | $`T`$ |
| `sensor/frameangvel/interval<sensor-frameangvel-interval>` | $`T`$ |
| `sensor/frameangvel/cutoff<sensor-frameangvel-cutoff>` | $`A\,T^{-1}`$ |
| `sensor/frameangvel/noise<sensor-frameangvel-noise>` | $`A\,T^{-1}`$ |
| `sensor/frameangvel/user<sensor-frameangvel-user>` | *other* |
| `sensor/framelinacc/delay<sensor-framelinacc-delay>` | $`T`$ |
| `sensor/framelinacc/interval<sensor-framelinacc-interval>` | $`T`$ |
| `sensor/framelinacc/cutoff<sensor-framelinacc-cutoff>` | $`L\,T^{-2}`$ |
| `sensor/framelinacc/noise<sensor-framelinacc-noise>` | $`L\,T^{-2}`$ |
| `sensor/framelinacc/user<sensor-framelinacc-user>` | *other* |
| `sensor/frameangacc/delay<sensor-frameangacc-delay>` | $`T`$ |
| `sensor/frameangacc/interval<sensor-frameangacc-interval>` | $`T`$ |
| `sensor/frameangacc/cutoff<sensor-frameangacc-cutoff>` | $`A\,T^{-2}`$ |
| `sensor/frameangacc/noise<sensor-frameangacc-noise>` | $`A\,T^{-2}`$ |
| `sensor/frameangacc/user<sensor-frameangacc-user>` | *other* |
| `sensor/subtreecom/delay<sensor-subtreecom-delay>` | $`T`$ |
| `sensor/subtreecom/interval<sensor-subtreecom-interval>` | $`T`$ |
| `sensor/subtreecom/cutoff<sensor-subtreecom-cutoff>` | $`L`$ |
| `sensor/subtreecom/noise<sensor-subtreecom-noise>` | $`L`$ |
| `sensor/subtreecom/user<sensor-subtreecom-user>` | *other* |
| `sensor/subtreelinvel/delay<sensor-subtreelinvel-delay>` | $`T`$ |
| `sensor/subtreelinvel/interval<sensor-subtreelinvel-interval>` | $`T`$ |
| `sensor/subtreelinvel/cutoff<sensor-subtreelinvel-cutoff>` | $`L\,T^{-1}`$ |
| `sensor/subtreelinvel/noise<sensor-subtreelinvel-noise>` | $`L\,T^{-1}`$ |
| `sensor/subtreelinvel/user<sensor-subtreelinvel-user>` | *other* |
| `sensor/subtreeangmom/delay<sensor-subtreeangmom-delay>` | $`T`$ |
| `sensor/subtreeangmom/interval<sensor-subtreeangmom-interval>` | $`T`$ |
| `sensor/subtreeangmom/cutoff<sensor-subtreeangmom-cutoff>` | $`M\,L^{2}\,T^{-1}`$ |
| `sensor/subtreeangmom/noise<sensor-subtreeangmom-noise>` | $`M\,L^{2}\,T^{-1}`$ |
| `sensor/subtreeangmom/user<sensor-subtreeangmom-user>` | *other* |
| `sensor/insidesite/delay<sensor-insidesite-delay>` | $`T`$ |
| `sensor/insidesite/interval<sensor-insidesite-interval>` | $`T`$ |
| `sensor/insidesite/cutoff<sensor-insidesite-cutoff>` | *varies* |
| `sensor/insidesite/noise<sensor-insidesite-noise>` | *varies* |
| `sensor/insidesite/user<sensor-insidesite-user>` | *other* |
| `sensor/distance/delay<sensor-distance-delay>` | $`T`$ |
| `sensor/distance/interval<sensor-distance-interval>` | $`T`$ |
| `sensor/distance/cutoff<sensor-distance-cutoff>` | $`L`$ |
| `sensor/distance/noise<sensor-distance-noise>` | $`L`$ |
| `sensor/distance/user<sensor-distance-user>` | *other* |
| `sensor/normal/delay<sensor-normal-delay>` | $`T`$ |
| `sensor/normal/interval<sensor-normal-interval>` | $`T`$ |
| `sensor/normal/cutoff<sensor-normal-cutoff>` | $`1`$ |
| `sensor/normal/noise<sensor-normal-noise>` | $`1`$ |
| `sensor/normal/user<sensor-normal-user>` | *other* |
| `sensor/fromto/delay<sensor-fromto-delay>` | $`T`$ |
| `sensor/fromto/interval<sensor-fromto-interval>` | $`T`$ |
| `sensor/fromto/cutoff<sensor-fromto-cutoff>` | $`L`$ |
| `sensor/fromto/noise<sensor-fromto-noise>` | $`L`$ |
| `sensor/fromto/user<sensor-fromto-user>` | *other* |
| `sensor/contact/delay<sensor-contact-delay>` | $`T`$ |
| `sensor/contact/interval<sensor-contact-interval>` | $`T`$ |
| `sensor/contact/cutoff<sensor-contact-cutoff>` | *varies* |
| `sensor/contact/noise<sensor-contact-noise>` | *varies* |
| `sensor/contact/user<sensor-contact-user>` | *other* |
| `sensor/e_potential/delay<sensor-e_potential-delay>` | $`T`$ |
| `sensor/e_potential/interval<sensor-e_potential-interval>` | $`T`$ |
| `sensor/e_potential/cutoff<sensor-e_potential-cutoff>` | $`M\,L^{2}\,T^{-2}`$ |
| `sensor/e_potential/noise<sensor-e_potential-noise>` | $`M\,L^{2}\,T^{-2}`$ |
| `sensor/e_potential/user<sensor-e_potential-user>` | *other* |
| `sensor/e_kinetic/delay<sensor-e_kinetic-delay>` | $`T`$ |
| `sensor/e_kinetic/interval<sensor-e_kinetic-interval>` | $`T`$ |
| `sensor/e_kinetic/cutoff<sensor-e_kinetic-cutoff>` | $`M\,L^{2}\,T^{-2}`$ |
| `sensor/e_kinetic/noise<sensor-e_kinetic-noise>` | $`M\,L^{2}\,T^{-2}`$ |
| `sensor/e_kinetic/user<sensor-e_kinetic-user>` | *other* |
| `sensor/clock/delay<sensor-clock-delay>` | $`T`$ |
| `sensor/clock/interval<sensor-clock-interval>` | $`T`$ |
| `sensor/clock/cutoff<sensor-clock-cutoff>` | $`T`$ |
| `sensor/clock/noise<sensor-clock-noise>` | $`T`$ |
| `sensor/clock/user<sensor-clock-user>` | *other* |
| `sensor/tactile/delay<sensor-tactile-delay>` | $`T`$ |
| `sensor/tactile/interval<sensor-tactile-interval>` | $`T`$ |
| `sensor/tactile/cutoff<sensor-tactile-cutoff>` | *varies* |
| `sensor/tactile/user<sensor-tactile-user>` | *other* |
| `sensor/user/cutoff<sensor-user-cutoff>` | *other* |
| `sensor/user/noise<sensor-user-noise>` | *other* |
| `sensor/user/user<sensor-user-user>` | *other* |
| `sensor/plugin/cutoff<sensor-plugin-cutoff>` | *other* |
| `sensor/plugin/user<sensor-plugin-user>` | *other* |
| `custom/numeric/data<custom-numeric-data>` | *other* |
| `tuple/element/prm<tuple-element-prm>` | *other* |
| `keyframe/key/time<keyframe-key-time>` | $`T`$ |
| `keyframe/key/qpos<keyframe-key-qpos>` | *varies* |
| `keyframe/key/qvel<keyframe-key-qvel>` | *varies* |
| `keyframe/key/act<keyframe-key-act>` | *varies* |
| `keyframe/key/mpos<keyframe-key-mpos>` | $`L`$ |
| `keyframe/key/mquat<keyframe-key-mquat>` | $`1`$ |
| `keyframe/key/ctrl<keyframe-key-ctrl>` | *varies* |
| `keyframe/key/plastic<keyframe-key-plastic>` | *varies* |


### XSD schema

The schema is also emitted as an [XML Schema](https://www.w3.org/TR/xmlschema-1/) (XSD) document, generated from the same source of truth and checked in as [src/xml/generated/mjcf.xsd](https://github.com/google-deepmind/mujoco/blob/main/src/xml/generated/mjcf.xsd). Editors use it to complete elements, attributes and keywords, and to report ill-formed values as you type:

<img src="images/XMLreference/xsd_editor.png" class="only-light only-lightalign-center" style="width:100.0%" alt="image" />

<img src="images/XMLreference/xsd_editor_dark.png" class="only-dark only-darkalign-center" style="width:100.0%" alt="image" />

To enable this in VS Code, install the Red Hat [XML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml) (or the same extension from [Open VSX](https://open-vsx.org/extension/redhat/vscode-xml) in forks such as Cursor and VSCodium) and reference the schema in the model's root element ([example](https://github.com/google-deepmind/mujoco/blob/main/test/xml/testdata/schema_location.xml)):

``` xml
<mujoco xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/google-deepmind/mujoco/refs/heads/main/src/xml/generated/mjcf.xsd">
```

Alternatively, associate model files with the schema in the editor's settings, leaving the models untouched:

``` json
"xml.fileAssociations": [{
  "pattern": "**/*.xml",
  "systemId": "https://raw.githubusercontent.com/google-deepmind/mujoco/refs/heads/main/src/xml/generated/mjcf.xsd"
}]
```

Replace `refs/heads/main` with a release tag to pin the schema to a MuJoCo version.

The XSD is not a specification of model validity: it never rejects a model that MuJoCo accepts, but does accept models that the compiler rejects. Constraints that XSD 1.0 cannot express -- child cardinality and presence constraints between attributes -- are carried as annotations.

## MJCF Reference

MJCF files have a unique top-level element [mujoco](XMLreference.md). The next-level elements are referred to as *sections*. They are all optional. Some sections are merely used for grouping and have no attributes. Sections can be repeated, to facilitate merging of models via the [include](XMLreference.md) element. The *order* of attributes within an element can be arbitrary. The order of child elements within a parent element can also be arbitrary, with four exceptions:

- The order of [joint](XMLreference.md) elements within a [body](XMLreference.md) matters because joint transformations are performed in sequence.
- The order of elements in a [spatial](XMLreference.md) tendon matters because it determines the sequence of objects that the tendon passes through or wraps around.
- The order of repeated sections matters when the same attribute is set multiple times to different values. In that case the last setting takes effect for the entire model.
- The order of multiple actuator elements in the same defaults class matters, because a class has a single actuator default and each shortcut resets its gain, bias and dynamics parameters; see [Shortcuts](modeling.md).

In the remainder of this chapter we describe all valid MJCF elements and their attributes. Some elements can be used in multiple contexts, in which case their meaning depends on the parent element. This is why we always show the parent as a prefix in the documentation below.

### Meta elements

These elements are not strictly part of the low-level MJCF format definition, but rather instruct the compiler to perform some operation on the model. A general property of meta-elements is that they disappear from the model upon saving the XML; the exception is [frame](XMLreference.md), which is preserved. There are currently five meta-elements in MJCF:

- [include](XMLreference.md), [frame](XMLreference.md), and [replicate](XMLreference.md) which are outside of the schema.
- [flexcomp](XMLreference.md) and [attach](XMLreference.md) which are part of the schema, but serve to procedurally generate other MJCF elements.

#### **frame** `sync`

The frame meta-element is a pure coordinate transformation that can wrap any group of elements in the kinematic tree (under [worldbody](XMLreference.md)). At compile time the transformation is accumulated into the frame's direct children; frames have no counterpart in [mjModel](APIreference/APItypes.md). Unlike the other meta-elements, frames are preserved when the model is saved: the frame is written with its pose and its contents in frame-relative coordinates, so a saved model reloads with the same frames. The attributes of the frame meta-element are documented [below](XMLreference.md).

#### **replicate** `sync`

The replicate element duplicates the enclosed kinematic tree elements with incremental translational and rotational offsets, adding namespace suffixes to avoid name collisions. Appended suffix strings are integers in the range `[0...count-1]` with the minimum number of digits required to represent the total element count (i.e., if replicating 200 times, suffixes will be `000, 001, ...` etc). All referencing elements are automatically replicated and namespaced appropriately. Detailed examples of models using replicate can be found in the [model/replicate/](https://github.com/google-deepmind/mujoco/tree/main/model/replicate) directory.

Direct children of replicate are replicated into its parent body. Joints are therefore not allowed as direct children; wrap them in a [body](XMLreference.md).

[Keyframes](XMLreference.md) are not replicated: a keyframe describes the model with all replicas in place, so its vectors follow the layout of the compiled model. If the enclosed tree contains [attach](XMLreference.md) elements, the keyframes of the attached model are added once, namespaced by the <span class="el">attach</span> element only, and set the state of the first replica. See the limitations discussed in [attachment](programming/modeledit.md).


<span class="at">count</span>: <span class="at-val">int, required</span>  
The number of replicas. Must be positive.



<span class="at">sep</span>: <span class="at-val">string, optional</span>  
The namespace separator. This optional string is prepended to the namespace suffix string. Note that for nested replicate elements, the innermost namespace suffixes are appended first.



<span class="at">offset</span>: <span class="at-val">real(3), optional</span>  
Translational offset along the three coordinate axes. In general, the frame of the offset is with respect to the previous replica, except for the first one which is with respect to the replicate element's parent. If there is no rotation, these values are always in the frame of the replicate element's parent.



<span class="at">euler</span>: <span class="at-val">real(3), optional</span>  
Rotation angles around three coordinate axes between two subsequent replicas. The angular units and rotation sequence respect the global [angle](XMLreference.md) and [eulerseq](XMLreference.md) settings. Rotation is always with respect to the frame of the previous replica, so total rotation is cumulative.



Usage example of replicate

Loading this model and saving it:

``` xml
<mujoco>
  <worldbody>
    <replicate count="2" offset="0 1 0" euler="90 0 0">
      <replicate count="2" sep="-" offset="1 0 0" euler="0 90 0">
        <geom name="Alice" size=".1"/>
      </replicate>
    </replicate>
  </worldbody>

  <sensor>
    <accelerometer name="Bob" site="Alice"/>
  </sensor>
</mujoco>
```

Results in this model:

``` xml
<mujoco>
  <worldbody>
    <geom name="Alice-00" size="0.1"/>
    <geom name="Alice-10" size="0.1" pos="1 0 0" quat="1 0 1 0"/>
    <geom name="Alice-01" size="0.1" pos="0 1 0" quat="1 1 0 0"/>
    <geom name="Alice-11" size="0.1" pos="1 1 0" quat="0.5 0.5 0.5 0.5"/>
  </worldbody>

  <sensor>
    <accelerometer name="Bob-00" site="Alice-00"/>
    <accelerometer name="Bob-10" site="Alice-10"/>
    <accelerometer name="Bob-01" site="Alice-01"/>
    <accelerometer name="Bob-11" site="Alice-11"/>
  </sensor>
</mujoco>
```


#### **include** ​

This element does not strictly belong to MJCF. Instead it is a meta-element, used to assemble multiple XML files in a single document object model (DOM) before parsing. The included file must be a valid XML file with a unique top-level element. This top-level element is removed by the parser, and the elements below it are inserted at the location of the <span class="el">include</span> element. At least one element must be inserted as a result of this procedure. The <span class="el">include</span> element can be used wherever an XML element is expected in the MJCF file. Nested includes are allowed, however a given XML file can be included at most once in the entire model. After all the included XML files have been assembled into a single DOM, it must correspond to a valid MJCF model. Other than that, it is up to the user to decide how to use includes and how to modularize large files if desired.

<span class="at">file</span>: <span class="at-val">string, required</span>  
The name of the XML file to be included. The file location is relative to the directory of the main MJCF file. If the file is not in the same directory, it should be prefixed with a relative path.


Prefer attach to include

While some use cases for [include](XMLreference.md) remain valid, it is recommended to use the [attach](XMLreference.md) element instead, where applicable.


### **mujoco** `star`

The unique top-level element, identifying the XML file as an MJCF model file.


<span class="at">model</span>: <span class="at-val">string, "MuJoCo Model"</span>  
The name of the model. This name is shown in the title bar of [simulate.cc](programming/samples.md).


### **option** ​

This element is in one-to-one correspondence with the low level structure mjOption contained in the field mjModel.opt of mjModel. These are simulation options and do not affect the compilation process in any way; they are simply copied into the low level model. Even though mjOption can be modified by the user at runtime, it is nevertheless a good idea to adjust it properly through the XML.


<span class="at">timestep</span>: <span class="at-val">real, "0.002"</span>  
Simulation time step in seconds. This is the single most important parameter affecting the speed-accuracy trade-off which is inherent in every physics simulation. Smaller values result in better accuracy and stability. To achieve real-time performance, the time step must be larger than the CPU time per step (or 4 times larger when using the RK4 integrator). The CPU time is measured with internal timers. It should be monitored when adjusting the time step. MuJoCo can simulate most robotic systems a lot faster than real-time, however models with many floating objects (resulting in many contacts) are more demanding computationally. Keep in mind that stability is determined not only by the time step but also by the [Solver parameters](modeling.md); in particular softer constraints can be simulated with larger time steps. When fine-tuning a challenging model, it is recommended to experiment with both settings jointly. In optimization-related applications, real-time is no longer good enough and instead it is desirable to run the simulation as fast as possible. In that case the time step should be made as large as possible.



<span class="at">impratio</span>: <span class="at-val">real, "1"</span>  
This attribute determines the ratio of frictional-to-normal constraint impedance for elliptic friction cones. The setting of solimp determines a single impedance value for all contact dimensions, which is then modulated by this attribute. Settings larger than 1 cause friction forces to be "harder" than normal forces, having the general effect of reducing [slow slippage](modeling.md) without increasing the actual friction coefficient or guaranteeing exact sticking. For pyramidal friction cones the situation is more complex because the pyramidal approximation mixes normal and frictional dimensions within each basis vector; it is not recommended to use high impratio values with pyramidal cones.



<span class="at">gravity</span>: <span class="at-val">real(3), "0 0 -9.81"</span>  
Gravitational acceleration vector. In the default world orientation the Z-axis points up. The MuJoCo GUI is organized around this convention (both the camera and perturbation commands are based on it) so we do not recommend deviating from it.



<span class="at">wind</span>: <span class="at-val">real(3), "0 0 0"</span>  
Velocity vector of the medium (i.e., wind). This vector is subtracted from the 3D translational velocity of each body, and the result is used to compute viscous, lift and drag forces acting on the body; recall [Passive forces](computation/index.md) in the Computation chapter. The magnitude of these forces scales with the values of the next two attributes.



<span class="at">magnetic</span>: <span class="at-val">real(3), "0 -0.5 0"</span>  
Global magnetic flux. This vector is used by magnetometer sensors, which are defined as sites and return the magnetic flux at the site position expressed in the site frame.



<span class="at">density</span>: <span class="at-val">real, "0"</span>  
Density of the medium, not to be confused with the geom density used to infer masses and inertias. This parameter is used to simulate lift and drag forces, which scale quadratically with velocity. In SI units the density of air is around 1.2 while the density of water is around 1000 depending on temperature. Setting density to 0 disables lift and drag forces.



<span class="at">viscosity</span>: <span class="at-val">real, "0"</span>  
Viscosity of the medium. This parameter is used to simulate viscous forces, which scale linearly with velocity. In SI units the viscosity of air is around 0.00002 while the viscosity of water is around 0.0009 depending on temperature. Setting viscosity to 0 disables viscous forces. Note that the default Euler [integrator](computation/index.md) handles damping in the joints implicitly – which improves stability and accuracy. It does not presently do this with body viscosity. Therefore, if the goal is merely to create a damped simulation (as opposed to modeling the specific effects of viscosity), we recommend using joint damping rather than body viscosity, or switching to the <span class="at">implicit</span> or <span class="at">implicitfast</span> integrators.



<span class="at">o_margin</span>: <span class="at-val">real, "0"</span>  
This attribute replaces the margin parameter of all active contact pairs when [Contact override](modeling.md) is enabled. Otherwise MuJoCo uses the element-specific margin attribute of [geom](XMLreference.md) or [pair](XMLreference.md) depending on how the contact pair was generated. See [margin and gap](computation/index.md) in the Computation chapter. The related gap parameter does not have a global override.





<span class="at">o_solref</span>, <span class="at">o_solimp</span>, <span class="at">o_friction</span>  
These attributes replace the solref, solimp and friction parameters of all active contact pairs when contact override is enabled. See [Solver parameters](modeling.md) for details.





<span class="at">integrator</span>: <span class="at-val">\[Euler, RK4, implicit, implicitfast, discrete\], "Euler"</span>  
This attribute selects the numerical [integrator](computation/index.md) to be used. Currently the available integrators are the semi-implicit Euler method, the fixed-step 4th-order Runge-Kutta method, the implicit-in-velocity Euler method, <span class="at">implicitfast</span>, which drops the Coriolis and centrifugal terms, and <span class="at">discrete</span>, a velocity-stepping integrator which unifies constraint solving and implicit position/velocity updates in an effective inertia metric. See [Numerical Integration](computation/index.md) for more details.



<span class="at">cone</span>: <span class="at-val">\[pyramidal, elliptic\], "pyramidal"</span>  
The type of contact friction cone. Elliptic cones are a better model of the physical reality, but pyramidal cones sometimes make the solver faster and more robust.



<span class="at">jacobian</span>: <span class="at-val">\[dense, sparse, auto\], "auto"</span>  
The type of constraint Jacobian and matrices computed from it. Auto resolves to dense when the number of degrees of freedom is up to 60, and sparse over 60.



<span class="at">solver</span>: <span class="at-val">\[PGS, CG, Newton\], "Newton"</span>  
This attribute selects one of the constraint solver [algorithms](computation/index.md) described in the Computation chapter. Guidelines for solver selection and parameter tuning are available in the [Algorithms](modeling.md) section above.



<span class="at">iterations</span>: <span class="at-val">int, "100"</span>  
Maximum number of iterations of the constraint solver. When the warmstart attribute of [flag](XMLreference.md) is enabled (which is the default), accurate results are obtained with fewer iterations; if the warmstarted solution already satisfies the tolerance, the CG and Newton solvers terminate with zero iterations. Larger and more complex systems with many interacting constraints require more iterations. Note that mjData.solver contains statistics about solver convergence, also shown in the profiler.



<span class="at">tolerance</span>: <span class="at-val">real, "1e-8"</span>  
Tolerance threshold used for early termination of the iterative solver. For PGS, the threshold is applied to the cost improvement between two iterations. For CG and Newton, it is applied to the smaller of the cost improvement and the gradient norm. For Newton, it is additionally applied to the Newton decrement $`\tfrac{1}{2} g^T H^{-1} g`$, the predicted cost improvement of the next iteration. Before the first iteration, CG and Newton also apply it to a [convergence certificate](computation/index.md) of the warmstarted solution, possibly terminating with zero iterations. The cost improvement and the gradient are scaled by the inverse trace of the inertia matrix, of the whole model or of a constraint [island](computation/index.md). Set the tolerance to 0 to disable early termination.



<span class="at">ls_iterations</span>: <span class="at-val">int, "50"</span>  
Maximum number of linesearch iterations performed by CG/Newton constraint solvers. Ensures that at most [iterations](XMLreference.md) times [ls_iterations](XMLreference.md) linesearch iterations are performed during each constraint solve.



<span class="at">ls_tolerance</span>: <span class="at-val">real, "0.01"</span>  
Tolerance threshold used for early termination of the linesearch algorithm.



<span class="at">noslip_iterations</span>: <span class="at-val">int, "0"</span>  
Maximum number of iterations of the NoSlip solver. This is a post-processing step executed after the main solver. It uses a modified PGS method to suppress slip/drift in friction dimensions resulting from the soft-constraint model. The default setting 0 disables this post-processing step. See the [NoSlip solver](computation/index.md) for its mechanics and tradeoffs, and [slow slippage](modeling.md) for practical guidance.



<span class="at">noslip_tolerance</span>: <span class="at-val">real, "1e-6"</span>  
Tolerance threshold used for early termination of the Noslip solver.



<span class="at">ccd_iterations</span>: <span class="at-val">int, "35"</span>  
Maximum number of iterations of the algorithm used for convex collisions. This rarely needs to be adjusted, except in situations where some geoms have very large aspect ratios.



<span class="at">ccd_tolerance</span>: <span class="at-val">real, "1e-6"</span>  
Tolerance threshold used for early termination of the convex collision algorithm.



<span class="at">sleep_tolerance</span>: <span class="at-val">real, "1e-3"</span>  
Velocity tolerance below which [sleeping](computation/index.md) is allowed.



<span class="at">sdf_iterations</span>: <span class="at-val">int, "10"</span>  
Number of iterations used for Signed Distance Field collisions (per initial point).



<span class="at">sdf_initpoints</span>: <span class="at-val">int, "40"</span>  
Number of starting points used for finding contacts with Signed Distance Field collisions.



H9qG9Zf2W44



<span class="at">actuatorgroupdisable</span>: <span class="at-val">int(31), optional</span>  
List of actuator groups to disable. Actuators whose [group](XMLreference.md) is in this list will produce no force. If they are stateful, their activation states will not be integrated. Internally this list is implemented as an integer bitfield, so values must be in the range `0 <= group <= 30`. If not set, all actuator groups are enabled. See [example model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/actuation/actuator_group_disable.xml) and associated screen-capture on the right.


#### <span class="el-prefix">option/</span> ⁠ **flag** `dot`

This element sets the flags that enable and disable different parts of the simulation pipeline. The actual flags used at runtime are represented as the bits of two integers, namely mjModel.opt.disableflags and mjModel.opt.enableflags, used to disable standard features and enable optional features respectively. The reason for this separation is that setting both integers to 0 restores the default. In the XML we do not make this separation explicit, except for the default attribute values - which are "enable" for flags corresponding to standard features, and "disable" for flags corresponding to optional features. In the documentation below, we explain what happens when the setting is different from its default.


<span class="at">constraint</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables all standard computations related to the constraint solver. As a result, no constraint forces are applied. Note that the next four flags disable the computations related to a specific type of constraint. Both this flag and the type-specific flag must be set to "enable" for a given computation to be performed.



<span class="at">equality</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables all standard computations related to equality constraints.



<span class="at">frictionloss</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables all standard computations related to friction loss constraints.



<span class="at">limit</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables all standard computations related to joint and tendon limit constraints.



<span class="at">contact</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables collision detection and all standard computations related to contact constraints.



<span class="at">spring</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables passive joint, tendon and flex springs. If passive [damper](XMLreference.md) forces are also disabled, **all** passive forces are disabled, including gravity compensation, fluid forces, forces computed by the [mjcb_passive](APIreference/APIglobals.md) callback, and forces computed by [plugins](programming/extension.md) when passed the [mjPLUGIN_PASSIVE](APIreference/APItypes.md) capability flag.



<span class="at">damper</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables passive joint, tendon and flex dampers. If passive [spring](XMLreference.md) forces are also disabled, **all** passive forces are disabled, including gravity compensation, fluid forces, forces computed by the [mjcb_passive](APIreference/APIglobals.md) callback, and forces computed by [plugins](programming/extension.md) when passed the [mjPLUGIN_PASSIVE](APIreference/APItypes.md) capability flag.



<span class="at">gravity</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag causes the gravitational acceleration vector in mjOption to be replaced with (0 0 0) at runtime, without changing the value in mjOption. Once the flag is re-enabled, the value in mjOption is used.



<span class="at">clampctrl</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables the clamping of control inputs to all actuators, even if the actuator-specific attributes are set to enable clamping.



<span class="at">warmstart</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables warm-starting of the constraint solver. By default the solver uses the solution (i.e., the constraint force) from the previous time step to initialize the iterative optimization. This feature should be disabled when evaluating the dynamics at a collection of states that do not form a trajectory - in which case warm starts make no sense and are likely to slow down the solver.



<span class="at">filterparent</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables the filtering of contact pairs where the two geoms belong to a parent and child body; recall contact [selection](computation/index.md) in the Computation chapter.



<span class="at">actuation</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables all standard computations related to actuator forces, including the actuator dynamics. As a result, no actuator forces are applied to the simulation.



<span class="at">refsafe</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag enables a safety mechanism that prevents instabilities due to solref\[0\] being too small compared to the simulation timestep. Recall that solref\[0\] is the stiffness of the virtual spring-damper used for constraint stabilization. If this setting is enabled, the solver uses max(solref\[0\], 2\*timestep) in place of solref\[0\] separately for each active constraint. Under the [discrete](computation/index.md) integrator, the flag instead replaces contact and limit rows whose spring the timestep cannot resolve (solref\[0\]\*solref\[1\] \< timestep) by the stiffest zero-restitution row for the timestep, keeping the authored damping ratio.



<span class="at">sensor</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables all computations related to sensors. When disabled, sensor values will remain constant, either zeros if disabled at the start of simulation, or, if disabled at runtime, whatever value was last computed.



<span class="at">midphase</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables the mid-phase collision filtering using a static AABB bounding volume hierarchy (a BVH binary tree). If disabled, all geoms pairs that are allowed to collide are checked for collisions.



<span class="at">nativeccd</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag enables the native convex collision detection pipeline instead of using the [libccd library](https://github.com/danfis/libccd), see [convex collisions](computation/index.md) for more details.



<span class="at">island</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag enables discovery and construction of constraint islands: disjoint sets of constraints and degrees-of-freedom that do not interact and can be solved independently. Islanding is not yet supported by the PGS solver. See [Constraint islands](computation/index.md) for more details. The [mjVIS_ISLAND](APIreference/APItypes.md) enables [island visualization](https://youtu.be/Vc1tq0fFvQA).



<span class="at">eulerdamp</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables implicit integration with respect to joint damping in the Euler integrator. See the [Numerical Integration](computation/index.md) section for more details.



<span class="at">autoreset</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag disables the automatic resetting of the simulation state when numerical issues are detected.



<span class="at">override</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag enables the [Contact override](modeling.md) mechanism.



<span class="at">energy</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag enables the computation of potential and kinetic energy in `mjData.energy[0, 1]` respectively, and displayed in the simulate GUI info overlay. Potential energy includes the gravitational component summed over all bodies $`\sum_b m_b g h`$ and energy stored in passive springs in joints, tendons and flexes $`\tfrac{1}{2} k x^2`$, where $`x`$ is the displacement and $`k`$ is the spring constant. Kinetic energy is given by $`\tfrac{1}{2} v^T M v`$, where $`v`$ is the velocity and $`M`$ is the mass matrix. Note that potential and kinetic energy in constraints is not accounted for.

The extra computation (also triggered by [potential](XMLreference.md) and [kinetic](XMLreference.md) energy sensors) adds some CPU time but it is usually negligible. Monitoring energy for a system that is supposed to be energy-conserving is one of the best ways to assess the accuracy of a complex simulation.



<span class="at">fwdinv</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag enables the automatic comparison of forward and inverse dynamics. When enabled, the inverse dynamics is invoked after mj_forward (or internally within mj_step) and the difference in applied forces is recorded in mjData.solver_fwdinv\[2\]. The first value is the relative norm of the discrepancy in joint space, the next is in constraint space.



<span class="at">invdiscrete</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag enables discrete-time inverse dynamics with *mj_inverse* for all [integrators](XMLreference.md) other than `RK4`. Recall from the [numerical integration](computation/index.md) section that the one-step integrators (`Euler`, `implicit` and `implicitfast`), modify the mass matrix $`M \rightarrow M-hD`$. This implies that finite-differenced accelerations $`(v_{t+h} - v_t)/h`$ will not correspond to the continuous-time acceleration `mjData.qacc`. When this flag is enabled, *mj_inverse* will interpret `qacc` as having been computed from the difference of two sequential velocities, and undo the above modification.



<span class="at">multiccd</span>: <span class="at-val">\[disable, enable\], "enable"</span>  
This flag enables multiple-contact collision detection for geom pairs that use a general-purpose convex-convex collider e.g., mesh-mesh collisions. This can be useful when the contacting geoms have a flat surface and the single contact point generated by the convex-convex collider cannot accurately capture the surface contact, leading to instabilities that typically manifest as sliding or wobbling. The implementation of this feature depends on the selected convex collision pipeline, see [convex collisions](computation/index.md) for more details.



<span class="at">sleep</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag enables [sleeping](computation/index.md). Disabling this flag when some trees are sleeping will wake them.


flag value at initialization time

Unlike any other [flag](XMLreference.md), the <span class="at">sleep</span> flag has an effect during [mjData](APIreference/APItypes.md) **initialization** (*mj_makeData* or *mj_resetData*). First, it must be set at initialization time in order for the [sleep-init](XMLreference.md) policy to take effect. Second, it must be set in order for static quantities to be computed. See [implementation notes](programming/simulation.md) for more details.




<span class="at">diagexact</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag enables computation of the exact diagonal of the constraint-space inertia matrix $`A = J M^{-1} J^T`$, replacing the body-based approximation normally used. The exact diagonal is computed from the whitened Jacobian $`Y = J M^{-1/2}`$ as $`A_{ii} = \|Y_i\|^2`$. This provides a more accurate [impedance](computation/index.md) computation, which can improve solver quality for models with complex kinematic coupling. See [Diagonal approximation](computation/index.md) for details on the approximation errors that this flag eliminates. The cost is one back-substitution with the Cholesky factor of the mass matrix per active constraint row; if dual solvers are used ([PGS](XMLreference.md) or [NoSlip](XMLreference.md)), the cost is negligible since $`Y`$ is computed anyway. Consider enabling this flag when observing divergence or poor constraint quality, particularly in models with highly anisotropic body inertias or bodies operating far from the initial configuration `qpos0`.

Under the `discrete` [integrator](XMLreference.md), the exact diagonal is computed against the factored backbone of the effective metric $`\widehat{M}`$; tendon, actuator and flex couplings are not included.



<span class="at">ipc</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag selects the IPC contact mode of the `discrete` [integrator](XMLreference.md); it is an error with any other integrator. The mode is experimental. It keeps contact multipliers in [mjData](APIreference/APItypes.md) across steps that no [state specification](APIreference/APItypes.md) covers, so *mj_getState* and *mj_setState* do not capture its full state and exact replay from a saved state is not supported. The mode solves its subproblems with a primal solver (`Newton` by default, or `CG`), so [solver](XMLreference.md) cannot be `PGS`, and it cannot be combined with the `fwdinv` or `sleep` flags. It applies model-wide: every flex the mode supports has its contact solved this way. Contacts between two supported flexes, and between a supported flex and a static plane, sphere, capsule, box or mesh, are resolved by the mode and the collision pipeline does not generate them; contacts with moving bodies and with the other geom types keep their constraint rows. The pairs the mode resolves are frictionless: they carry normal forces only, and the friction parameters of the flexes and geoms involved do not apply to them. The usual collision filtering applies to the pairs the mode resolves: none with the `contact` flag disabled, the contype/conaffinity rule of contact [selection](computation/index.md) between a flex and a geom or between two flexes, and each flex's `selfcollide` for its self-contact. A pinned flex vertex may ride a static body or a body reached through slide joints only, whose points move on the straight segments the mode sweeps; a hinge, ball or free joint on that chain is an error. The mode assumes metre-scale models with millimetre-thick flexes: its detection band, rest gap between flex surfaces and convergence speed are fixed at 3 mm, 1 mm and 0.05 m/s. Contact is passive under this flag whatever [passive](XMLreference.md) says, since the flag replaces the penalty form of passive contact — the same contact law with the multiplier held at zero — with the augmented-Lagrangian solve, rather than returning any flex to the constraint solver. Flex contact is solved by a barrier-free augmented-Lagrangian outer loop around the discrete solve: each step minimizes an incremental potential subject to linearized contact constraints, carried as one-sided rows of the constraint solver whose multipliers are updated between solves, re-linearizing contact at trial positions, and every committed position update is verified intersection-free by continuous collision detection, so flex contact cannot tunnel. Rigid bodies are carried through the same position-level step with their contacts kept in the constraint solver, and a model without 2D flexes takes that step as well. Supported for dim-2 flexes: a flex with edge equality constraints keeps its elasticity in the constraint solver, while [elastic2d](XMLreference.md) elasticity is integrated implicitly through the effective metric. Under this flag the constraint stage of *mj_forward* is skipped for a model with a 2D flex: after *mj_forward*, `mjData.qacc` holds the free-flight acceleration and the acceleration-stage sensors are computed from it. The step recomputes those sensors from its own acceleration and constraint force before it commits, so after *mj_step* they read as under the plain `discrete` integrator; a user or plugin sensor at the acceleration stage is evaluated twice per step. Inverse dynamics is not supported.



<span class="at">speculative</span>: <span class="at-val">\[disable, enable\], "disable"</span>  
This flag enables speculative contacts for fast-moving convex geoms, adding contacts before impact to prevent tunneling through thin obstacles within a single timestep. See [speculative contacts](computation/index.md) for more details.


### **compiler** ​

This element is used to set options for the built-in parser and compiler. After parsing and compilation it no longer has any effect. The settings here are global and apply to the entire model.


<span class="at">autolimits</span>: <span class="at-val">\[false, true\], "true"</span>  
This attribute affects the behavior of attributes such as "limited" (on \<body-joint\> or \<tendon\>), "forcelimited", "ctrllimited", and "actlimited" (on \<actuator\>). If "true", these attributes are unnecessary and their value will be inferred from the presence of their corresponding "range" attribute. If "false", no such inference will happen: For a joint to be limited, both limited="true" and range="min max" must be specified. In this mode, it is an error to specify a range without a limit.



<span class="at">boundmass</span>: <span class="at-val">real, "0"</span>  
This attribute imposes a lower bound on the mass of each body except for the world body. Setting this attribute to a value greater than 0 can be used as a quick fix for poorly designed models that contain massless moving bodies, such as the dummy bodies often used in URDF models to attach sensors. Note that in MuJoCo there is no need to create dummy bodies.



<span class="at">boundinertia</span>: <span class="at-val">real, "0"</span>  
This attribute imposes a lower bound on the diagonal inertia components of each body except for the world body. Its use is similar to boundmass above.



<span class="at">settotalmass</span>: <span class="at-val">real, "-1"</span>  
This attribute is deprecated and will be removed in a future release; compiling a model which sets it gives a warning. If this value is positive, the compiler will scale the masses and inertias of all bodies in the model, so that the total mass equals the value specified here. The world body has mass 0 and does not participate in any mass-related computations. This scaling is performed last, after all other operations affecting the body mass and inertia. The same scaling operation can be applied at runtime to the compiled mjModel with the function *mj_setTotalmass*, followed by *mj_setConst*.



<span class="at">balanceinertia</span>: <span class="at-val">\[false, true\], "false"</span>  
A valid diagonal inertia matrix must satisfy A+B\>=C for all permutations of the three diagonal elements. Some poorly designed models violate this constraint, which will normally result in a compile error. If this attribute is set to "true", the compiler will silently set all three diagonal elements to their average value whenever the above condition is violated.



<span class="at">strippath</span>: <span class="at-val">\[false, true\], "false"</span>  
When this attribute is "true", the parser will remove any path information in file names specified in the model. This is useful for loading models created on a different system using a different directory structure. File names that match a registered [resource provider](programming/extension.md) (for example `custom://path/to/file.obj`) are not filesystem paths and are left untouched, so the provider receives the full name.



<span class="at">coordinate</span>: <span class="at-val">\[local, global\], "local"</span>  
This attribute specifies whether frame positions and orientations are expressed in local coordinates. The "global" option is no longer supported and will cause an error.



<span class="at">angle</span>: <span class="at-val">\[radian, degree\], "degree" for MJCF, always "radian" for URDF</span>  
This attribute specifies whether the angles in the MJCF model are expressed in units of degrees or radians. The compiler converts degrees into radians, and mjModel always uses radians. For URDF models the parser sets this attribute to "radian" internally, regardless of the XML setting.


<img src="images/changelog/meshfit.png" class="align-right" style="width:40.0%" alt="image" />


<span class="at">fitaabb</span>: <span class="at-val">\[false, true\], "false"</span>  
The compiler is able to replace a mesh with a geometric primitive fitted to that mesh; see [geom](XMLreference.md) below. If this attribute is "true", the fitting procedure uses the axis-aligned bounding box (AABB) of the mesh, choosing the smallest primitive whose AABB contains the mesh AABB. Otherwise it uses the equivalent-inertia box of the mesh. The type of geometric primitive used for fitting is specified separately for each geom. The models used to generate the image on the right can be found [here](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/fitmesh_inertiabox.xml) (fit inertia box) and [here](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/fitmesh_aabb.xml) (fit aabb).



<span class="at">eulerseq</span>: <span class="at-val">string, "xyz"</span>  
This attribute specifies the sequence of Euler rotations for all <span class="at">euler</span> attributes of elements that have spatial frames, as explained in [Frame orientations](modeling.md). This must be a string with exactly 3 characters from the set {x, y, z, X, Y, Z}. The character at position n determines the axis around which the n-th rotation is performed. Lower case letters denote axes that rotate with the frame (intrinsic), while upper case letters denote axes that remain fixed in the parent frame (extrinsic). The "rpy" convention used in URDF corresponds to "XYZ" in MJCF.



<span class="at">meshdir</span>: <span class="at-val">string, optional</span>  
This attribute instructs the compiler where to look for mesh and height field files. The full path to a file is determined as follows. If the strippath attribute described above is "true", all path information from the file name is removed. The following checks are then applied in order: (1) if the file name contains an absolute path, it is used without further changes; (2) if this attribute is set and contains an absolute path, the full path is the string given here appended with the file name; (3) the full path is the path to the main MJCF model file, appended with the value of this attribute if specified, appended with the file name.



<span class="at">texturedir</span>: <span class="at-val">string, optional</span>  
This attribute is used to instruct the compiler where to look for texture files. It works in the same way as meshdir above.



<span class="at">assetdir</span>: <span class="at-val">string, optional</span>  
This attribute sets the values of both <span class="at">meshdir</span> and <span class="at">texturedir</span> above. Values in the latter attributes take precedence over <span class="at">assetdir</span>.



<span class="at">discardvisual</span>: <span class="at-val">\[false, true\], "false" for MJCF, "true" for URDF</span>  
This attribute instructs the compiler to discard all model elements which are purely visual and have no effect on the physics (with one exception, see below). This often enables smaller [mjModel](APIreference/APItypes.md) structs and faster simulation.

- All materials and textures are discarded, unless they are referenced by a sensor or a custom [tuple](XMLreference.md).
- All geoms with [contype](XMLreference.md) ⁠ = ⁠ [conaffinity](XMLreference.md) ⁠ =0 are discarded, if they are not referenced in another MJCF element and do not use the ellipsoid [fluid model](XMLreference.md). If a discarded geom was used for inferring body inertia, an explicit [inertial](XMLreference.md) element is added to the body. This is not possible when [inertiafromgeom](XMLreference.md) is "true", which is then a compilation error.
- All meshes which are not used by a remaining geom or by a site, and are not referenced in another MJCF element, are discarded (in particular those of the geoms discarded above).

The resulting compiled model will have exactly the same dynamics as the original model. The only engine-level computation which might change is the output of *raycasting* computations, as used for example by [rangefinder](XMLreference.md) sensors, since raycasting reports distances to visual geoms. When visualizing models compiled with this flag, it is important to remember that collision geoms are often placed in a [group](XMLreference.md) which is invisible by default.

Discarding is an operation on the model itself, *mjs_discardVisual*, which is applied before compiling. A model which is saved or compiled again afterwards is the one without the visual elements.



<span class="at">usethread</span>: <span class="at-val">\[false, true\], "true"</span>  
If this attribute is "true", the model compiler will run in multi-threaded mode. Multi-threading is used for computing the length ranges of actuators and for parallel loading and processing of meshes.



<span class="at">fusestatic</span>: <span class="at-val">\[false, true\], "false" for MJCF, "true" for URDF</span>  
This attribute controls a compiler optimization feature where static bodies are fused with their parent, and any elements defined in those bodies are reassigned to the parent. Static bodies are fused with their parent unless

- They are referenced by another element in the model.
- They contain a site which is referenced by a [force](XMLreference.md) or [torque](XMLreference.md) sensor.
- Their [fuse](XMLreference.md) attribute is "false".
- They have a [plugin](XMLreference.md) or a [sleep](XMLreference.md) policy.
- They have mass, and either a [gravcomp](XMLreference.md) different from that of their parent, or the model is in a fluid (non-zero [density](XMLreference.md) or [viscosity](XMLreference.md)); in a fluid, bodies with an ellipsoid-fluid geom are kept too.
- [inertiafromgeom](XMLreference.md) is "true" and the compiler adjusted their inertia or their parent's ([boundmass](XMLreference.md), [boundinertia](XMLreference.md), [balanceinertia](XMLreference.md)), so that the geoms of both in one body would have a different inertia.

Fusing is an operation on the model itself, *mjs_fuseStatic*, which is applied before compiling: each fused body becomes a [frame](XMLreference.md) in its parent. A model which is saved or compiled again afterwards is the fused one.

This optimization is particularly useful when importing URDF models which often have many dummy bodies, but can also be used to optimize MJCF models. After optimization, the new model has identical kinematics and dynamics as the original but is faster to simulate.



<span class="at">inertiafromgeom</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
This attribute controls the automatic inference of body masses and inertias from geoms attached to the body. If this setting is "false", no automatic inference is performed. In that case each body must have explicitly defined mass and inertia with the [inertial](XMLreference.md) element, or else a compile error will be generated. If this setting is "true", the mass and inertia of each body will be inferred from the geoms attached to it, overriding any values specified with the <span class="el">inertial</span> element. The default setting "auto" means that masses and inertias are inferred automatically only when the <span class="el">inertial</span> element is missing in the body definition. One reason to set this attribute to "true" instead of "auto" is to override inertial data imported from a poorly designed model. In particular, a number of publicly available URDF models have seemingly arbitrary inertias which are too large compared to the mass. This results in equivalent inertia boxes which extend far beyond the geometric boundaries of the model. Note that the built-in OpenGL visualizer can render equivalent inertia boxes.



<span class="at">alignfree</span>: <span class="at-val">\[false, true\], "false"</span>  
This attribute toggles the default behaviour of an optimization that applies to bodies with a [free joint](XMLreference.md) and no child bodies. When true, the body frame and free joint will automatically be aligned with inertial frame, which leads to both faster and more stable simulation. See [freejoint/align](XMLreference.md) for details.



<span class="at">inertiagrouprange</span>: <span class="at-val">int(2), "0 5"</span>  
This attribute specifies the range of geom groups that are used to infer body masses and inertias (when such inference is enabled). The group attribute of [geom](XMLreference.md) is an integer. If this integer falls in the range specified here, the geom will be used in the inertial computation, otherwise it will be ignored. This feature is useful in models that have redundant sets of geoms for collision and visualization. Note that the world body does not participate in the inertial computations, so any geoms attached to it are automatically ignored. Therefore it is not necessary to adjust this attribute and the geom-specific groups so as to exclude world geoms from the inertial computation.



<span class="at">saveinertial</span>: <span class="at-val">\[false, true\], "false"</span>  
If set to "true", the compiler will save explicit [inertial](XMLreference.md) clauses for all bodies.



<span class="at">savecompiled</span>: <span class="at-val">\[false, true\], "true"</span>  
This attribute and the next one say how the model is saved as MJCF; like <span class="at">saveinertial</span>, they are not saved themselves. If "true", the values which compilation made of the model are saved: for example the size of a geom which was fitted to a mesh, or the pose of a body after [alignment](XMLreference.md) with its free joint. If "false", the model is saved as it is written in the [mjSpec](APIreference/APItypes.md), and the saved file compiles to the same model; the spec need not have been compiled.



<span class="at">savecanonical</span>: <span class="at-val">\[false, true\], "true"</span>  
If "true", orientations are saved as quaternions, angles in radians, sizes and poses which were given with <span class="at">fromto</span> as <span class="at">size</span>, <span class="at">pos</span> and <span class="at">quat</span>, a <span class="at">fullinertia</span> as <span class="at">diaginertia</span> and <span class="at">quat</span>, and every actuator as <span class="el">general</span>. If "false", they are saved in the notation in which they were written. This attribute has an effect only if [savecompiled](XMLreference.md) is "false": compiled values are always saved in the canonical notation.



<span class="at">conflict</span>: <span class="at-val">\[warning, merge, error\], "warning"</span>  
This attribute controls how conflicting global attributes (physics options, sizes, visual settings) are resolved when a child spec is attached to a parent using *mjs_attach*. A conflict occurs when both the parent and child specify authored values for the same field and those values differ. See [Attribute Merging](programming/modeledit.md) for details and a per-field table.

<span class="at-val">warning</span>  
Parent values take precedence. When a conflict is detected, a warning is emitted but the parent value is not modified. This is the default and preserves the pre-existing attachment behavior.

<span class="at-val">merge</span>  
Fields are merged using field-specific strategies (minimum, maximum, OR, or error), depending on the field's semantics. When only the child specifies an authored value, it is adopted by the parent. See the *merging table* for per-field details.

<span class="at-val">error</span>  
Any conflict between authored values results in a compile error. This is the strictest mode and is useful for detecting unintended attribute mismatches.



<span class="at">passthrough</span>: <span class="at-val">\[none, textures\], "none"</span>  
Which assets the compiler leaves [by reference](modeling.md) instead of loading into [mjModel](APIreference/APItypes.md). With "textures", a texture loaded from a single file is not read: the model holds its resolved path and the parameters a consumer needs to load it, and no pixels. Textures which the compiler would transform (flipped, composite [grids](XMLreference.md), six [separate files](XMLreference.md)), procedural textures, textures given as a buffer and files served from memory by a *virtual file system* stay embedded. The per-texture [embed](XMLreference.md) attribute overrides this policy. The policy is that of the model being compiled, so it also applies to the textures of [attached](XMLreference.md) models. Only textures can be by reference for now; other asset types will be added to the list of values.


#### <span class="el-prefix">compiler/</span> ⁠ **lengthrange** `dot`

This element controls the computation of actuator length ranges. For an overview of this functionality see [Length range](modeling.md) section. Note that if this element is omitted the defaults shown below still apply. In order to disable length range computations altogether, include this element and set mode="none".


<span class="at">mode</span>: <span class="at-val">\[none, muscle, muscleuser, all\], "muscle"</span>  
Determines the type of actuators to which length range computation is applied. "none" disables this functionality. "all" applies it to all actuators. "muscle" applies it to actuators whose gaintype or biastype is set to "muscle". "muscleuser" applies it to actuators whose gaintype or biastype is set to either "muscle" or "user". The default is "muscle" because MuJoCo's muscle model requires actuator length ranges to be defined.



<span class="at">useexisting</span>: <span class="at-val">\[false, true\], "true"</span>  
If this attribute is "true" and the length range for a given actuator is already defined in the model, the existing value will be used and the automatic computation will be skipped. The range is considered defined if the first number is smaller than the second number. The only reason to set this attribute to "false" is to force re-computation of actuator length ranges - which is needed when the model geometry is modified. Note that the automatic computation relies on simulation and can be slow, so saving the model with the values which compilation made ([savecompiled](XMLreference.md)) and using the existing values when possible is recommended.



<span class="at">uselimit</span>: <span class="at-val">\[false, true\], "false"</span>  
If this attribute is "true" and the actuator is attached to a joint or a tendon which has limits defined, these limits will be copied into the actuator length range and the automatic computation will be skipped. This may seem like a good idea but note that in complex models the feasible range of tendon actuators depends on the entire model, and may be smaller than the user-defined limits for that tendon. So the safer approach is to set this to "false", and let the automatic computation discover the feasible range.



<span class="at">accel</span>: <span class="at-val">real, "20"</span>  
This attribute scales the forces applied to the simulation in order to push each actuator to its smallest and largest length. The force magnitude is computed so that the resulting joint-space acceleration vector has norm equal to this attribute.



<span class="at">maxforce</span>: <span class="at-val">real, "0"</span>  
The force computed via the accel attribute above can be very large when the actuator has very small moments. Such a force will still produce reasonable acceleration (by construction) but large numbers could cause numerical issues. Although we have never observed such issues, the present attribute is provided as a safeguard. Setting it to a value larger than 0 limits the norm of the force being applied during simulation. The default setting of 0 disables this safeguard.



<span class="at">timeconst</span>: <span class="at-val">real, "1"</span>  
The simulation is damped in a non-physical way so as to push the actuators to their limits without the risk of instabilities. This is done by simply scaling down the joint velocity at each time step. In the absence of new accelerations, such scaling will decrease the velocity exponentially. The timeconst attribute specifies the time constant of this exponential decrease, in seconds.



<span class="at">timestep</span>: <span class="at-val">real, "0.01"</span>  
The timestep used for the internal simulation. Setting this to 0 will cause the model timestep to be used. The latter is not the default because models that can go unstable usually have small timesteps, while the simulation here is artificially damped and very stable. To speed up the length range computation, users can attempt to increase this value.



<span class="at">inttotal</span>: <span class="at-val">real, "10"</span>  
The total time interval (in seconds) for running the internal simulation, for each actuator and actuator direction. Each simulation is initialized at qpos0. It is expected to settle after inttotal time has passed.



<span class="at">interval</span>: <span class="at-val">real, "2"</span>  
The time interval at the end of the simulation over which length data is collected and analyzed. The maximum (or respectively minimum) length achieved during this interval is recorded. The difference between the maximum and minimum is also recorded and is used as a measure of divergence. If the simulation settles, this difference will be small. If it is not small, this could be because the simulation has not yet settled - in which case the above attributes should be adjusted - or because the model does not have sufficient joint and tendon limits and so the actuator range is effectively unlimited. Both of these conditions cause the same compiler error. Recall that contacts are disabled in this simulation, so joint and tendon limits as well as overall geometry are the only things that can prevent actuators from having infinite length.



<span class="at">tolrange</span>: <span class="at-val">real, "0.05"</span>  
This determines the threshold for detecting divergence and generating a compiler error. The range of actuator lengths observed during interval is divided by the overall range computed via simulation. If that value is larger than tolrange, a compiler error is generated. So one way to suppress compiler errors is to simply make this attribute larger, but in that case the results could be inaccurate.


### **size** ​

This element specifies size parameters that cannot be inferred from the number of elements in the model. Unlike the fields of mjOption which can be modified at runtime, sizes are structural parameters and should not be modified after compilation.


<span class="at">memory</span>: <span class="at-val">string, "-1"</span>  
This attribute specifies the size of memory allocated for dynamic arrays in the `mjData.arena` memory space, in bytes. The default setting of `-1` instructs the compiler to guess how much space to allocate. Appending the digits with one of the letters {K, M, G, T, P, E} sets the unit to be {kilo, mega, giga, tera, peta, exa}-byte, respectively. Thus "16M" means "allocate 16 megabytes of `arena` memory". If the Newton solver runs out of `arena` memory while building its Hessian or Cholesky factor (for example under heavy flex contact fill-in), it raises `mjWARN_CNSTRFULL` and falls back to CG for that step; increase `memory` if this warning persists. See the [Memory allocation](modeling.md) section for details.



<span class="at">njmax</span>: <span class="at-val">int, "-1"</span> |nbsp| |nbsp| |nbsp| (legacy)  
This is a deprecated legacy attribute. It previously determined the maximum allowed number of constraints. Currently it means "allocate as much memory as would have previously been required for this number of constraints". Specifying both <span class="at">njmax</span> and <span class="at">memory</span> leads to an error.



<span class="at">nconmax</span>: <span class="at-val">int, "-1"</span> |nbsp| |nbsp| |nbsp| (legacy)  
This attribute specifies the maximum number of contacts that will be generated at runtime. If the number of active contacts is about to exceed this value, the extra contacts are discarded and a warning is generated. This is a deprecated legacy attribute which previously affected memory allocation. It is kept for backwards compatibility and debugging purposes.



<span class="at">nstack</span>: <span class="at-val">int, "-1"</span> |nbsp| |nbsp| |nbsp| (legacy)  
This is a deprecated legacy attribute. It previously determined the maximum size of the [stack](programming/simulation.md). If <span class="at">nstack</span> is specified, then the size of `mjData.narena` is `nstack * sizeof(mjtNum)` bytes, plus an additional space for the constraint solver. Specifying both <span class="at">nstack</span> and <span class="at">memory</span> leads to an error.



<span class="at">nuserdata</span>: <span class="at-val">int, "0"</span>  
The size of the field mjData.userdata of mjData. This field should be used to store custom dynamic variables. See also [User parameters](modeling.md).



<span class="at">nkey</span>: <span class="at-val">int, "0"</span>  
The number of key frames allocated in mjModel is the larger of this value and the number of [key](XMLreference.md) elements below. Note that the interactive simulator has the ability to take snapshots of the system state and save them as key frames.



<span class="at">nuser_body</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each body. See also [User parameters](modeling.md). The parameter values are set via the user attribute of the [body](XMLreference.md) element. These values are not accessed by MuJoCo. They can be used to define element properties needed in user callbacks and other custom code.



<span class="at">nuser_jnt</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each [joint](XMLreference.md).



<span class="at">nuser_geom</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each [geom](XMLreference.md).



<span class="at">nuser_site</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each [site](XMLreference.md).



<span class="at">nuser_cam</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each [camera](XMLreference.md).



<span class="at">nuser_tendon</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each [tendon](XMLreference.md).



<span class="at">nuser_actuator</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each [actuator](XMLreference.md).



<span class="at">nuser_sensor</span>: <span class="at-val">int, "-1"</span>  
The number of custom user parameters added to the definition of each [sensor](XMLreference.md).


### **statistic** ​

This element is used to override model statistics computed by the compiler. These statistics are not only informational but are also used to scale various components of the rendering and perturbation. We provide an override mechanism in the XML because it is sometimes easier to adjust a small number of model statistics than a larger number of visual parameters.


<span class="at">meanmass</span>: <span class="at-val">real, optional</span>  
If this attribute is specified, it replaces the value of mjModel.stat.meanmass computed by the compiler. The computed value is the average body mass, not counting the massless world body. At runtime this value scales the perturbation force.



<span class="at">meaninertia</span>: <span class="at-val">real, optional</span>  
This attribute is deprecated and will be removed in a future release; compiling a model which sets it gives a warning. If it is specified, it replaces the value of mjModel.stat.meaninertia computed by the compiler. The computed value is the average diagonal element of the joint-space inertia matrix when the model is in qpos0. It does not affect simulation: the solvers scale their termination criteria by the trace of the current inertia matrix, see [tolerance](XMLreference.md).



<span class="at">meansize</span>: <span class="at-val">real, optional</span>  
If this attribute is specified, it replaces the value of `mjModel.stat.meansize` computed by the compiler. At runtime this value multiplies the attributes of the [scale](XMLreference.md) element above, and acts as their length unit. If specific lengths are desired, it can be convenient to set <span class="at">meansize</span> to a round number like 1 or 0.01 so that [scale](XMLreference.md) values are in recognized length units. This is the only semantic of <span class="at">meansize</span> and setting it has no other side-effect. The automatically computed value is heuristic, representing the average body radius. The heuristic is based on geom sizes when present, the distances between joints when present, and the sizes of the body equivalent inertia boxes.



<span class="at">extent</span>: <span class="at-val">real, optional</span>  
If this attribute is specified, it replaces the value of mjModel.stat.extent computed by the compiler. The computed value is half the side of the bounding box of the model in the initial configuration. At runtime this value is multiplied by some of the attributes of the [map](XMLreference.md) element above. When the model is first loaded, the free camera's initial distance from the <span class="at">center</span> (see below) is 1.5 times the <span class="at">extent</span>. Must be strictly positive.



<span class="at">center</span>: <span class="at-val">real(3), optional</span>  
If this attribute is specified, it replaces the value of mjModel.stat.center computed by the compiler. The computed value is the center of the bounding box of the entire model in the initial configuration. This 3D vector is used to center the view of the free camera when the model is first loaded.


### **asset** ​

This is a grouping element for defining assets. It does not have attributes. Assets are created in the model so that they can be referenced from other model elements; recall the discussion of [Assets](overview.md) in the Overview chapter. Assets opened from a file can be identified in two different ways: filename extensions or the `content_type` attribute. MuJoCo will attempt to open a file specified by the content type provided, and only defaults to the filename extension if no `content_type` attribute is specified. The content type is ignored if the asset isn't loaded from a file.

#### <span class="el-prefix">asset/</span> ⁠ **mesh** ​

This element creates a mesh asset, which can then be referenced from geoms. If the referencing geom type is <span class="at-val">mesh</span> the mesh is instantiated in the model, otherwise a geometric primitive is automatically fitted to it; see the [geom](XMLreference.md) element below.

MuJoCo works with triangulated meshes. They can be loaded from binary STL files, OBJ files or MSH files with custom format described below, or vertex and face data specified directly in the XML. Software such as MeshLab can be used to convert from other mesh formats to STL or OBJ. While any collection of triangles can be loaded as a mesh and rendered, collision detection works with the convex hull of the mesh as explained in [Collision detection](computation/index.md). The mesh appearance (including texture mapping) is controlled by the <span class="at">material</span> and <span class="at">rgba</span> attributes of the referencing geom, similarly to height fields.

Meshes can have explicit texture coordinates instead of relying on the automated texture mapping mechanism. When provided, these explicit coordinates have priority. Note that texture coordinates can be specified with OBJ files and MSH files, as well as explicitly in the XML with the <span class="at">texcoord</span> attribute, but not via STL files. These mechanism cannot be mixed. So if you have an STL mesh, the only way to add texture coordinates to it is to convert to one of the other supported formats.



Legacy MSH file format

The binary MSH file starts with 4 integers specifying the number of vertex positions (nvertex), vertex normals (nnormal), vertex texture coordinates (ntexcoord), and vertex indices making up the faces (nface), followed by the numeric data. nvertex must be at least 4. nnormal and ntexcoord can be zero (in which case the corresponding data is not defined) or equal to nvertex. nface can also be zero, in which case faces are constructed automatically from the convex hull of the vertex positions. The file size in bytes must be exactly: 16 + 12\*(nvertex + nnormal + nface) + 8\*ntexcoord. The contents of the file must be as follows:

``` Text
(int32)   nvertex
(int32)   nnormal
(int32)   ntexcoord
(int32)   nface
(float)   vertex_positions[3*nvertex]
(float)   vertex_normals[3*nnormal]
(float)   vertex_texcoords[2*ntexcoord]
(int32)   face_vertex_indices[3*nface]
```



Poorly designed meshes can display rendering artifacts. In particular, the shadow mapping mechanism relies on having some distance between front and back-facing triangle faces. If the faces are repeated, with opposite normals as determined by the vertex order in each triangle, this causes shadow aliasing. The solution is to remove the repeated faces (which can be done in MeshLab) or use a better designed mesh. Flipped faces are checked by MuJoCo for meshes specified as OBJ or XML and an error message is returned.

The size of the mesh is determined by the 3D coordinates of the vertex data in the mesh file, multiplied by the components of the <span class="at">scale</span> attribute below. Scaling is applied separately for each coordinate axis. Note that negative scaling values can be used to flip the mesh; this is a legitimate operation. The size parameters of the referencing geoms are ignored, similarly to height fields. We also provide a mechanism to translate and rotate the 3D coordinates, using the attributes [refpos](XMLreference.md) and [refquat](XMLreference.md).

A mesh can also be defined without faces (a point cloud essentially). In that case the convex hull is constructed automatically.This makes it easy to construct simple shapes directly in the XML. For example, a pyramid can be created as follows:

``` xml
<asset>
  <mesh name="tetrahedron" vertex="0 0 0  1 0 0  0 1 0  0 0 1"/>
</asset>
```

Positioning and orienting is complicated by the fact that vertex data in the source asset are often relative to coordinate frames whose origin is not inside the mesh. In contrast, MuJoCo expects the origin of a geom's local frame to coincide with the geometric center of the shape. We resolve this discrepancy by pre-processing the mesh in the compiler, so that it is centered around (0,0,0) and its principal axes of inertia are the coordinate axes. We save the translation and rotation offsets applied to the source asset in [mjModel.mesh_pos](APIreference/APItypes.md) and [mjModel.mesh_quat](APIreference/APItypes.md); these are required if one reads vertex data from the source and needs to re-apply the transform. These offsets are then composed with the referencing geom's position and orientation; see also the <span class="at">mesh</span> attribute of [geom](XMLreference.md) below. Fortunately most meshes used in robot models are designed in a coordinate frame centered at the joint. This makes the corresponding MJCF model intuitive: we set the body frame at the joint, so that the joint position is (0,0,0) in the body frame, and simply reference the mesh. Below is an MJCF model fragment of a forearm, containing all the information needed to put the mesh where one would expect it to be. The body position is specified relative to the parent body, namely the upper arm (not shown). It is offset by 35 cm which is the typical length of the human upper arm. If the mesh vertex data were not designed in the above convention, we would have to use the geom position and orientation (or the <span class="at">refpos</span>, <span class="at">refquat</span> mechanism) to compensate, but in practice this is rarely needed.

``` xml
<asset>
  <mesh file="forearm.stl"/>
</asset>

<body pos="0 0 0.35"/>
  <joint type="hinge" axis="1 0 0"/>
  <geom type="mesh" mesh="forearm"/>
</body>
```

The inertial computation mentioned above is part of an algorithm used not only to center and align the mesh, but also to infer the mass and inertia of the body to which it is attached. This is done by computing the centroid of the triangle faces, connecting each face with the centroid to form a triangular pyramid, computing the mass and signed inertia of all pyramids (considered solid, or hollow if <span class="at">shellinertia</span> is true) and accumulating them. The sign ensures that pyramids on the outside of the surfaces are subtracted, as can occur with concave geometries. This algorithm can be found in section 1.3.8 of Computational Geometry in C (Second Edition) by Joseph O'Rourke.

The full list of processing steps applied by the compiler to each mesh is as follows:

1.  For STL meshes, remove any repeated vertices and re-index the faces if needed. If the mesh is not STL, we assume that the desired vertices and faces have already been generated and do not apply removal or re-indexing;
2.  If vertex normals are not provided, generate normals automatically, using a weighted average of the surrounding face normals. If sharp edges are encountered, the renderer uses the face normals to preserve the visual information about the edge, unless [smoothnormal](XMLreference.md) is true. Note that normals cannot be provided with STL meshes;
3.  Scale, translate and rotate the vertices and normals, re-normalize the normals in case of scaling. Save these transformations in `mjModel.mesh_{pos, quat, scale}`.
4.  Construct the convex hull if specified;
5.  Find the centroid of all triangle faces, and construct the union-of-pyramids representation. Triangles whose area is too small (below the [mjMINVAL](APIreference/APIglobals.md) value of 1E-14) result in compile error;
6.  Compute the center of mass and inertia matrix of the union-of-pyramids. Use eigenvalue decomposition to find the principal axes of inertia. Center and align the mesh, saving the translational and rotational offsets for subsequent geom-related computations.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the mesh, used for referencing. If omitted, the mesh name equals the file name without the path and extension.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes (only scale in this case).



<span class="at">content_type</span>: <span class="at-val">string, optional</span>  
If the file attribute is specified, then this sets the [Media Type](https://www.iana.org/assignments/media-types/media-types.xhtml) (formerly known as MIME type) of the file to be loaded. Any filename extensions will be overloaded. Currently `model/vnd.mujoco.msh`, `model/obj`, and `model/stl` are supported.



<span class="at">file</span>: <span class="at-val">string, optional</span>  
The file from which the mesh will be loaded. The path is determined as described in the meshdir attribute of [compiler](XMLreference.md). The file extension must be "stl", "msh", or "obj" (not case sensitive) specifying the file type. If the file name is omitted, the vertex attribute becomes required.



<span class="at">scale</span>: <span class="at-val">real(3), "1 1 1"</span>  
This attribute specifies the scaling that will be applied to the vertex data along each coordinate axis. Negative values are allowed, resulting in flipping the mesh along the corresponding axis.



<span class="at">inertia</span>: <span class="at-val">\[convex, exact, legacy, shell\], "legacy"</span>  
This attribute controls how the mesh is used when mass and inertia are [inferred from geometry](XMLreference.md). The default value is <span class="at-val">legacy</span> for backward compatibility, but <span class="at-val">convex</span> is recommended.

<span class="at-val">convex</span>: Use the mesh's convex hull to compute volume and inertia, assuming uniform density.

<span class="at-val">exact</span>: Compute volume and inertia exactly, even for non-convex meshes. This algorithm requires a well-oriented, watertight mesh and will error otherwise.

<span class="at-val">legacy</span>: Use the legacy algorithm, leads to volume overcounting for non-convex meshes. Though currently the default to avoid breakages, it is not recommended.

<span class="at-val">shell</span>: Assume mass is concentrated on the surface of the mesh. Use the mesh's surface to compute the inertia, assuming uniform surface density.



<span class="at">smoothnormal</span>: <span class="at-val">\[false, true\], "false"</span>  
Controls the automatic generation of vertex normals when normals are not given explicitly. If true, smooth normals are generated by averaging the face normals at each vertex, with weight proportional to the face area. If false, faces at large angles relative to the average normal are excluded from the average. In this way, sharp edges (as in cube edges) are not smoothed.



<span class="at">maxhullvert</span>: <span class="at-val">int, "-1"</span>  
Maximum number of vertices in a mesh's convex hull. Currently this is implemented by asking qhull [to terminate](http://www.qhull.org/html/qh-optt.htm#TAn) after <span class="at">maxhullvert</span> vertices. The default value of -1 means "unlimited". Positive values must be larger than 3.



<span class="at">vertex</span>: <span class="at-val">real(3\*nvert), optional</span>  
Vertex 3D position data. You can specify position data in the XML using this attribute, or using a binary file, but not both.



<span class="at">normal</span>: <span class="at-val">real(3\*nvert), optional</span>  
Vertex 3D normal data. If specified, the number of normals must equal the number of vertices. The model compiler normalizes the normals automatically.



<span class="at">texcoord</span>: <span class="at-val">real(2\*nvert), optional</span>  
Vertex 2D texture coordinates, which are numbers between 0 and 1. If specified, the number of texture coordinate pairs must equal the number of vertices.



<span class="at">face</span>: <span class="at-val">int(3\*nface), optional</span>  
Faces of the mesh. Each face is a sequence of 3 vertex indices, in counter-clockwise order. The indices must be integers between 0 and nvert-1.



<span class="at">refpos</span>: <span class="at-val">real(3), "0 0 0"</span>  
Reference position relative to which the 3D vertex coordinates are defined. This vector is subtracted from the positions.



<span class="at">refquat</span>: <span class="at-val">real(4), "1 0 0 0"</span>  
Reference orientation relative to which the 3D vertex coordinates and normals are defined. The conjugate of this quaternion is used to rotate the positions and normals. The model compiler normalizes the quaternion automatically.



<span class="at">builtin</span>: <span class="at-val">string, optional</span>  
The mesh is generated by the compiler from a set of parameters specified in [params](XMLreference.md). When saved to XML, meshes produced this way are converted to explicit vertices. The Python bindings include [convenience methods](python.md) for generating these meshes. The available built-in types, their parameters and semantics are:

[<img src="images/XMLreference/s.png" class="align-right" style="width:23.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/makemesh.xml)

<span class="at-val">sphere</span> (subdivision)  
Repeated subdivisions of a unit icosahedron ("icosphere"). For $`s`$ subdivisions, this mesh has $`V = 2 + 10 \cdot 4^s`$ vertices and $`F = 20 \cdot 4^s`$ faces.

**subdivision**: integer in \[0-4\]: The number of subdivisions to apply to icosahedron faces.

[<img src="images/XMLreference/h.png" class="align-right" style="width:23.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/makemesh.xml)

<span class="at-val">hemisphere</span> (resolution)  
Quad-projected hemisphere. For resolution $`r`$, this mesh has $`4r`$ edges and vertices on the equator and a total of $`V = 2 + 2(r+1)(r+2)`$ vertices and $`F = 4(r+1)(r+2)`$ faces.

**resolution**: integer in \[0-10\]: Equator discretization of one hemisphere quadrant.

[<img src="images/XMLreference/c.png" class="align-right" style="width:23.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/makemesh.xml)

<span class="at-val">cone</span> (nvert, radius)  
The convex hull of a regular unit polygon at z = -1 and a unit polygon with the given radius at z = 1. If radius is 1, the mesh a prism. If radius is 0, only a single vertex is placed at (0, 0, 1) and the mesh is a discrete cone. If radius is positive, the mesh is a truncated discrete cone.

**nvert**: integer \>= 3: The number vertices in the polygon. <br/> **radius**: real in \[0, 1\]: The radius of the top face.

[<img src="images/XMLreference/ss.png" class="align-right" style="width:23.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/makemesh.xml)

<span class="at-val">supersphere</span> (resolution, e, n)  
A generalization of a sphere, also known as a superellipsoid (we use 'supersphere' since semiaxis rescaling is performed by the [scale](XMLreference.md) attribute). If the **n** and **e** parameters are both 1, the shape is a sphere. See [here](https://en.wikipedia.org/wiki/Superellipsoid) for more details.

**resolution** integer \>= 3: Longitude and latitude discretization. <br/> **e**: real \>= 0: The "east-west" exponent. <br/> **n**: real \>= 0: The "north-south" exponent.

[<img src="images/XMLreference/st.png" class="align-right" style="width:23.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/makemesh.xml)

<span class="at-val">supertorus</span> (resolution, radius, s, t)  
A generalization of a torus with major radius of 1 and given minor radius. If the **s** and **t** parameters are both 1, the shape is a torus. See [here](https://en.wikipedia.org/wiki/Supertoroid) for more details. Note that this shape is inherently non-convex, and the [standard caveats](computation/index.md) about mesh collisions apply.

**resolution** integer \>= 3: Discretization of both circumfrences. <br/> **radius**: real in (0, 1\]: The minor radius of the torus. <br/> **s**: real \> 0: The "squareness" of minor sections. <br/> **t**: real \> 0: The "squareness" of major sections.

[<img src="images/XMLreference/w.png" class="align-right" style="width:23.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/user/testdata/makemesh.xml)

<span class="at-val">wedge</span> (res_phi, res_theta, fov_phi, fov_theta, gamma)  
A slice of a unit spherical shell in spherical coordinates. This mesh is designed to be used by the [tactile sensor](XMLreference.md), which reports data at the vertices.

**res_phi**: integer \>= 0: The vertical resolution of the slice. <br/> **res_theta**: integer \>= 0: The horizontal resolution of the slice. <br/> **fov_phi**: real in (0, 180\]: The horizontal field of view (degrees). <br/> **fov_phi**: real in (0, 90): The vertical field of view (degrees). <br/> **gamma**: real in \[0, 1\]: Foveal deformation of the discretization.

<span class="at-val">plate</span> (res_x, res_y)  
A rectangular plate with given resolution in each dimension. This mesh is designed to be used by the [tactile sensor](XMLreference.md), which reports data at the vertices.

**res_x**: integer \> 0: The horizontal resolution of the plate. <br/> **res_y**: integer \> 0: The vertical resolution of the plate.

<span class="at-val">grid</span> (count\[3\], spacing\[3\], \[dim\])  
A regular grid of vertices. If `dim` is 3 (default), creates a volumetric tetrahedral mesh. If `dim` is 2, creates a triangulated 2D surface mesh.

**count**: 3 integers \> 0: Number of vertices along each axis; must be 1 along the axes beyond `dim`. <br/> **spacing**: 3 reals: Spacing between grid points along each axis. <br/> **dim**: optional integer in \[2, 3\] (default 3): Mesh dimensionality.

<span class="at-val">box</span> (count\[3\], spacing\[3\], \[dim\])  
A procedural box mesh. If `dim` is 3 (default), creates a volumetric tetrahedral mesh. If `dim` is 2, creates an open-top triangular surface mesh (the `+z` face is omitted).

**count**: 3 integers \>= 2: Grid resolution along each axis. <br/> **spacing**: 3 reals: Spacing along each axis. <br/> **dim**: optional integer in \[2, 3\] (default 3): Mesh dimensionality.

<span class="at-val">cylinder</span> (count\[3\], spacing\[3\], \[dim\])  
A procedural cylinder mesh. If `dim` is 3 (default), creates a volumetric tetrahedral mesh. If `dim` is 2, creates an open-top triangular surface mesh (the `+z` face is omitted).

**count**: 3 integers \>= 2: Grid resolution along each axis. <br/> **spacing**: 3 reals: Spacing along each axis. <br/> **dim**: optional integer in \[2, 3\] (default 3): Mesh dimensionality.

<span class="at-val">ellipsoid</span> (count\[3\], spacing\[3\], \[dim\])  
A procedural ellipsoid mesh. If `dim` is 3 (default), creates a volumetric tetrahedral mesh. If `dim` is 2, creates an open-top triangular surface mesh (the `+z` face is omitted).

**count**: 3 integers \>= 2: Grid resolution along each axis. <br/> **spacing**: 3 reals: Spacing along each axis. <br/> **dim**: optional integer in \[2, 3\] (default 3): Mesh dimensionality.

<span class="at-val">square</span> (count\[3\], spacing\[3\])  
A 2D triangulated square surface mesh.

**count**: 3 integers (first 2 must be \> 0, last must be 1): Number of vertices along the x and y axes. <br/> **spacing**: 3 reals: Spacing along each axis.

<span class="at-val">disc</span> (count\[3\], spacing\[3\])  
A 2D triangulated disc surface mesh.

**count**: 3 integers (first 2 must be \> 0, last must be 1): Number of vertices along the radial and angular directions. <br/> **spacing**: 3 reals: Spacing along each axis.



<span class="at">params</span>: <span class="at-val">real(nparam), optional</span>  
The parameters used to generate a builtin mesh. The number and type of parameters and their semantic depends on the mesh type. See [mesh/builtin](XMLreference.md) for details. The `square` and `disc` types, and the `grid`, `box`, `cylinder` and `ellipsoid` types with `dim` \< 3, change a <span class="at-val">legacy</span> [inertia](XMLreference.md) (including an explicit one) to <span class="at-val">shell</span>, since they have no volume.



<span class="at">material</span>: <span class="at-val">string, optional</span>  
Fallback material for mesh geoms that do not specify their own material.


##### <span class="el-prefix">mesh/</span> ⁠ **plugin** `dot`

Associate this mesh with an [engine plugin](programming/extension.md). Either <span class="at">plugin</span> or <span class="at">instance</span> are required.


<span class="at">plugin</span>: <span class="at-val">string, optional</span>  
Plugin identifier, used for implicit plugin instantiation.



<span class="at">instance</span>: <span class="at-val">string, optional</span>  
Instance name, used for explicit plugin instantiation.


#### <span class="el-prefix">asset/</span> ⁠ **hfield** ​

This element creates a height field asset, which can then be referenced from geoms with type "hfield". A height field, also known as terrain map, is a 2D matrix of elevation data. The data can be specified in one of three ways:

1.  The elevation data can be loaded from a PNG file. The image is converted internally to gray scale, and the intensity of each pixel is used to define elevation; white is high and black is low.

2.  The elevation data can be loaded from a binary file in the custom format described below. As with all other matrices used in MuJoCo, the data ordering is row-major, like pixels in an image. If the data size is nrow-by-ncol, the file must have 4\*(2+nrow\*ncol) bytes:

        (int32)   nrow
        (int32)   ncol
        (float32) data[nrow*ncol]

3.  The elevation data can be left undefined at compile time. This is done by specifying the attributes nrow and ncol. The compiler allocates space for the height field data in mjModel and sets it to 0. The user can then generate a custom height field at runtime, either programmatically or using sensor data.

Regardless of which method is used to specify the elevation data, the compiler always normalizes it to the range \[0 1\]. However if the data is left undefined at compile time and generated later at runtime, it is the user's responsibility to normalize it.\
The position and orientation of the height field is determined by the geom that references it. The spatial extent on the other hand is specified by the height field asset itself via the size attribute, and cannot be modified by the referencing geom (the geom size parameters are ignored in this case). The same approach is used for meshes below: positioning is done by the geom while sizing is done by the asset. This is because height fields and meshes involve sizing operations that are not common to other geoms.\
For collision detection, a height field is treated as a union of triangular prisms. Collisions between height fields and other geoms (except for planes and other height fields which are not supported) are computed by first selecting the sub-grid of prisms that could collide with the geom based on its bounding box, and then using the general convex collider. The number of possible contacts between a height field and a geom is limited to 50 ([mjMAXCONPAIR](APIreference/APIglobals.md)); any contacts beyond that are discarded. To avoid penetration due to discarded contacts, the spatial features of the height field should be large compared to the geoms it collides with.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the height field, used for referencing. If the name is omitted and a file name is specified, the height field name equals the file name without the path and extension.



<span class="at">content_type</span>: <span class="at-val">string, optional</span>  
If the file attribute is specified, then this sets the [Media Type](https://www.iana.org/assignments/media-types/media-types.xhtml) (formerly known as MIME types) of the file to be loaded. Any filename extensions will be overloaded. Currently `image/png` and `image/vnd.mujoco.hfield` are supported.



<span class="at">file</span>: <span class="at-val">string, optional</span>  
If this attribute is specified, the elevation data is loaded from the given file. If the file extension is ".png", not case-sensitive, the file is treated as a PNG file. Otherwise it is treated as a binary file in the above custom format. The number of rows and columns in the data are determined from the file contents. Loading data from a file and setting nrow or ncol below to non-zero values results is compile error, even if these settings are consistent with the file contents.



<span class="at">nrow</span>: <span class="at-val">int, "0"</span>  
This attribute and the next are used to allocate a height field in mjModel. If the <span class="at">elevation</span> attribute is not set, the elevation data is set to 0. This attribute specifies the number of rows in the elevation data matrix. The default value of 0 means that the data will be loaded from a file, which will be used to infer the size of the matrix.



<span class="at">ncol</span>: <span class="at-val">int, "0"</span>  
This attribute specifies the number of columns in the elevation data matrix.



<span class="at">elevation</span>: <span class="at-val">real(nrow\*ncol), optional</span>  
This attribute specifies the elevation data matrix. Values are automatically normalized to lie between 0 and 1 by first subtracting the minimum value and then dividing by the (maximum-minimum) difference, if not 0. If not provided, values are set to 0. Note that the row order of data in [mjModel](APIreference/APItypes.md) and [mjsHField](APIreference/APItypes.md) is flipped w.r.t. the order in XML i.e., it is bottom-to-top.



<span class="at">size</span>: <span class="at-val">real(4), required</span>  
<figure class="align-right">
<img src="images/XMLreference/peaks.png" width="350" />
</figure>

The four numbers here are (radius_x, radius_y, elevation_z, base_z). The height field is centered at the referencing geom's local frame. Elevation is in the +Z direction. The first two numbers specify the X and Y extent (or "radius") of the rectangle over which the height field is defined. This may seem unnatural for rectangles, but it is natural for spheres and other geom types, and we prefer to use the same convention throughout the model. The third number is the maximum elevation; it scales the elevation data which is normalized to \[0-1\]. Thus the minimum elevation point is at Z=0 and the maximum elevation point is at Z=elevation_z. The last number is the depth of a box in the -Z direction serving as a "base" for the height field. Without this automatically generated box, the height field would have zero thickness at places there the normalized elevation data is zero. Unlike planes which impose global unilateral constraints, height fields are treated as unions of regular geoms, so there is no notion of being "under" the height field. Instead a geom is either inside or outside the height field - which is why the inside part must have non-zero thickness. The example on the right is the MATLAB "peaks" surface saved in our custom height field format, and loaded as an asset with size = "1 1 1 0.1". The horizontal size of the box is 2, the difference between the maximum and minimum elevation is 1, and the depth of the base added below the minimum elevation point is 0.1.


#### <span class="el-prefix">asset/</span> ⁠ **skin** ​










[Skins](XMLreference.md) are grouped under the [deformable](XMLreference.md) element. Specifying them here is deprecated.










#### <span class="el-prefix">asset/</span> ⁠ **texture** ​

This element creates a texture asset, which is then referenced from a [material](XMLreference.md) asset, which is finally referenced from a model element that needs to be textured.

The texture data can be loaded from files or can be generated by the compiler as a procedural texture. Because different texture types require different parameters, only a subset of the attributes below are used for any given texture. Provisions are provided for loading cube and skybox textures from individual image files.

Two file formats are supported for loading textures: PNG and KTX. The loader will use the extension of the file name to determine which format to use. Alternatively, the content_type attribute can be used to specify the format explicitly. Only `image/png` and `image/ktx` are supported.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
As with all other assets, a texture must have a name in order to be referenced. However if the texture is loaded from a single file with the file attribute, the explicit name can be omitted and the file name (without the path and extension) becomes the texture name. If the name after parsing is empty and the texture type is not "skybox", the compiler will generate an error.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">type</span>: <span class="at-val">\[2d, cube, skybox\], "cube"</span>  
This attribute determines how the texture is represented and mapped to objects. It also determines which of the remaining attributes are relevant. The keywords have the following meaning:

The **cube** type has the effect of shrink-wrapping a texture cube over an object. Apart from the adjustment provided by the texuniform attribute of [material](XMLreference.md), the process is automatic. Internally the GPU constructs a ray from the center of the object to each pixel (or rather fragment), finds the intersection of this ray with the cube surface (the cube and the object have the same center), and uses the corresponding texture color. The six square images defining the cube can be the same or different; if they are the same, only one copy is stored in mjModel. There are four mechanisms for specifying the texture data:

1.  Single file (PNG or KTX) specified with the file attribute, containing a square image which is repeated on each side of the cube. This is the most common approach. If for example the goal is to create the appearance of wood, repeating the same image on all sides is sufficient.
2.  Single file containing a composite image from which the six squares are extracted by the compiler. The layout of the composite image is determined by the gridsize and gridlayout attributes.
3.  Six separate files specified with the attributes fileright, fileleft etc, each containing one square image.
4.  Procedural texture generated internally. The type of procedural texture is determined by the builtin attribute. The texture data also depends on a number of parameters documented below.

The **skybox** type is very similar to cube mapping, and in fact the texture data is specified in exactly the same way. The only difference is that the visualizer uses the first such texture defined in the model to render a skybox. This is a large box centered at the camera and always moving with it, with size determined automatically from the far clipping plane. The idea is that images on the skybox appear stationary, as if they are infinitely far away. If such a texture is referenced from a material applied to a regular object, the effect is equivalent to a cube map. Note however that the images suitable for skyboxes are rarely suitable for texturing objects.

The **2d** type maps a 2D image to a 3D object using [texture coordinates](XMLreference.md) (a.k.a UV coordinates). However, UV coordinates are only available for meshes. For primitive geoms, the texture is mapped to the object surface using the local XY coordinates of the geom, effectively projecting the texture along the Z axis. This sort of mapping is only suitable for planes and height fields, since their top surfaces always face the Z axis. 2d textures can be rectangular, unlike the sides of cube textures which must be square. The scaling can be controlled with the texrepeat attribute of [material](XMLreference.md). The data can be loaded from a single file or created procedurally.



<span class="at">colorspace</span>: <span class="at-val">\[auto, linear, sRGB\], "auto"</span>  
This attribute determines the color space of the texture. The default value `auto` means that the color space will be determined from the image file itself. If no color space is defined in the file, then `linear` is assumed.



<span class="at">content_type</span>: <span class="at-val">string, optional</span>  
If the file attribute is specified, then this sets the [Media Type](https://www.iana.org/assignments/media-types/media-types.xhtml) (formerly known as MIME types) of the file to be loaded. Any filename extensions will be ignored. Currently `image/png` and `image/ktx` are supported.



<span class="at">file</span>: <span class="at-val">string, optional</span>  
If this attribute is specified, and the builtin attribute below is set to "none", the texture data is loaded from a single file. See the texturedir attribute of [compiler](XMLreference.md) regarding the file path.



<span class="at">gridsize</span>: <span class="at-val">int(2), "1 1"</span>  
When a cube or skybox texture is loaded from a single file, this attribute and the next specify how the six square sides of the texture cube are obtained from the single image. The default setting "1 1" means that the same image is repeated on all sides of the cube. Otherwise the image is interpreted as a grid from which the six sides are extracted. The two integers here correspond to the number of rows and columns in the grid. Each integer must be positive and the product of the two cannot exceed 12. The number of rows and columns in the image must be integer multiples of the number of rows and columns in the grid, and these two multiples must be equal, so that the extracted images are square.



<span class="at">gridlayout</span>: <span class="at-val">string, "............"</span>  
<figure class="align-right">
<img src="images/XMLreference/skybox.png" width="250" />
</figure>

When a cube or skybox texture is loaded from a single file, and the grid size is different from "1 1", this attribute specifies which grid cells are used and which side of the cube they correspond to. There are many skybox textures available online as composite images, but they do not use the same convention, which is why we have designed a flexible mechanism for decoding them. The string specified here must be composed of characters from the set {'.', 'R', 'L', 'U', 'D', 'F', 'B'}. The number of characters must equal the product of the two grid sizes. Setting <span class="at">gridsize</span> to a value that differs from the inherited default without specifying <span class="at">gridlayout</span> resets <span class="at">gridlayout</span> to all `'.'`. The grid is scanned in row-major order. The '.' character denotes an unused cell. The other characters are the first letters of Right, Left, Up, Down, Front, Back; see below for coordinate frame description. If the symbol for a given side appears more than once, the last definition is used. If a given side is omitted, it is filled with the color specified by the rgb1 attribute. For example, the desert landscape below can be loaded as a skybox or a cube map using gridsize = "3 4" and gridlayout = ".U..LFRB.D.." The full-resolution image file without the markings can be downloaded [here](_static/desert.png).








<span class="at">fileright</span>, <span class="at">fileleft</span>, <span class="at">fileup</span>, <span class="at">filedown</span>, <span class="at">filefront</span>, <span class="at">fileback</span> : string, optional  
These attributes are used to load the six sides of a cube or skybox texture from separate files, but only if the file attribute is omitted and the builtin attribute is set to "none". If any one of these attributes are omitted, the corresponding side is filled with the color specified by the rgb1 attribute. The coordinate frame here is unusual. When a skybox is viewed with the default free camera in its initial configuration, the Right, Left, Up, Down sides appear where one would expect them. The Back side appears in front of the viewer, because the viewer is in the middle of the box and is facing its back. There is however a complication. In MuJoCo the +Z axis points up, while existing skybox textures (which are non-trivial to design) tend to assume that the +Y axis points up. Changing coordinates cannot be done by merely renaming files; instead one would have to transpose and/or mirror some of the images. To avoid this complication, we render the skybox rotated by 90 deg around the +X axis, in violation of our convention. However we cannot do the same for regular objects. Thus the mapping of skybox and cube textures on regular objects, expressed in the local frame of the object, is as follows: Right = +X, Left = -X, Up = +Y, Down = -Y, Front = +Z, Back = -Z.








<span class="at">builtin</span>: <span class="at-val">\[none, gradient, checker, flat\], "none"</span>  
This and the remaining attributes control the generation of procedural textures. If the value of this attribute is different from "none", the texture is treated as procedural and any file names are ignored. The keywords have the following meaning:

**gradient**  
Generates a color gradient from rgb1 to rgb2. The interpolation in color space is done through a sigmoid function. For cube and skybox textures the gradient is along the +Y axis, i.e., from top to bottom for skybox rendering.

**checker**  
Generates a 2-by-2 checker pattern with alternating colors given by rgb1 and rgb2. This is suitable for rendering ground planes and also for marking objects with rotational symmetries. Note that 2d textures can be scaled so as to repeat the pattern as many times as necessary. For cube and skybox textures, the checker pattern is painted on each side of the cube.

**flat**  
Fills the entire texture with rgb1, except for the bottom face of cube and skybox textures which is filled with rgb2.



<span class="at">rgb1</span>: <span class="at-val">real(3), "0.8 0.8 0.8"</span>  
The first color used for procedural texture generation. This color is also used to fill missing sides of cube and skybox textures loaded from files. The components of this and all other RGB(A) vectors should be in the range \[0 1\].



<span class="at">rgb2</span>: <span class="at-val">real(3), "0.5 0.5 0.5"</span>  
The second color used for procedural texture generation.



<span class="at">mark</span>: <span class="at-val">\[none, edge, cross, random\], "none"</span>  
Procedural textures can be marked with the markrgb color, on top of the colors determined by the builtin type. "edge" means that the edges of all texture images are marked. "cross" means that a cross is marked in the middle of each image. "random" means that randomly chosen pixels are marked. All markings are one-pixel wide, thus the markings appear larger and more diffuse on smaller textures.



<span class="at">markrgb</span>: <span class="at-val">real(3), "0 0 0"</span>  
The color used for procedural texture markings.



<span class="at">random</span>: <span class="at-val">real, "0.01"</span>  
When the mark attribute is set to "random", this attribute determines the probability of turning on each pixel. Note that larger textures have more pixels, and the probability here is applied independently to each pixel -- thus the texture size and probability need to be adjusted jointly. Together with a gradient skybox texture, this can create the appearance of a night sky with stars. The random number generator is initialized with a fixed seed.



<span class="at">width</span>: <span class="at-val">int, "0"</span>  
The width of a procedural texture, i.e., the number of columns in the image. Larger values usually result in higher quality images, although in some cases (e.g. checker patterns) small values are sufficient. For textures loaded from files, this attribute is ignored.



<span class="at">height</span>: <span class="at-val">int, "0"</span>  
The height of the procedural texture, i.e., the number of rows in the image. For cube and skybox textures, this attribute is ignored and the height is set to 6 times the width. For textures loaded from files, this attribute is ignored.



<span class="at">hflip</span>: <span class="at-val">\[false, true\], "false"</span>  
If true, images loaded from file are flipped in the horizontal direction. Does not affect procedural textures.



<span class="at">vflip</span>: <span class="at-val">\[false, true\], "false"</span>  
If true, images loaded from file are flipped in the vertical direction. Does not affect procedural textures.



<span class="at">nchannel</span>: <span class="at-val">int, "3"</span>  
The number of channels in the texture image file. This allows loading 4-channel textures (RGBA) or single-channel textures (e.g., for Physics-Based Rendering properties such as roughness or metallic). Procedural, cube and skybox textures must have 3 channels.



<span class="at">embed</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
Whether the pixels of this texture are in [mjModel](APIreference/APItypes.md) or the texture is left [by reference](modeling.md). "auto" follows the [passthrough](XMLreference.md) policy of the compiler. "true" keeps the pixels in the model whatever the policy says, for example for a texture which is written into at runtime. "false" asks for the texture to be by reference whatever the policy says, and is a compile error for a texture which cannot be: one which is procedural, given as a buffer or as six separate files, flipped, a composite grid, or whose file is served from memory by a *virtual file system*.


#### <span class="el-prefix">asset/</span> ⁠ **material** ​

This element creates a material asset. It can be referenced from [skins](XMLreference.md), [geoms](XMLreference.md), [sites](XMLreference.md) and [tendons](XMLreference.md) to set their appearance. Note that all these elements also have a local rgba attribute, which is more convenient when only colors need to be adjusted, because it does not require creating materials and referencing them. Materials are useful for adjusting appearance properties beyond color. However once a material is created, it is more natural the specify the color using the material, so that all appearance properties are grouped together.


<span class="at">name</span>: <span class="at-val">string, required</span>  
Name of the material, used for referencing.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">texture</span>: <span class="at-val">string, optional</span>  
If this attribute is specified, the material has a texture associated with it. Referencing the material from a model element will cause the texture to be applied to that element. Note that the value of this attribute is the name of a texture asset, not a texture file name. Textures cannot be loaded in the material definition; instead they must be loaded explicitly via the [texture](XMLreference.md) element and then referenced here. The texture referenced here is used for specifying the RGB values. For advanced rendering (e.g., Physics-Based Rendering), more texture types need to be specified (e.g., roughness, metallic). In this case, this texture attribute should be omitted, and the texture types should be specified using [layer](XMLreference.md) child elements. Note however that the built-in renderer does not support PBR properties, so these advanced rendering features are only available when using an external renderer.



<span class="at">texrepeat</span>: <span class="at-val">real(2), "1 1"</span>  
This attribute applies to textures of type "2d". It specifies how many times the texture image is repeated, relative to either the object size or the spatial unit, as determined by the next attribute.



<span class="at">texuniform</span>: <span class="at-val">\[false, true\], "false"</span>  
For cube textures, this attribute controls how cube mapping is applied. The default value "false" means apply cube mapping directly, using the actual size of the object. The value "true" maps the texture to a unit object before scaling it to its actual size (geometric primitives are created by the renderer as unit objects and then scaled). In some cases this leads to more uniform texture appearance, but in general, which settings produces better results depends on the texture and the object. For 2d textures, this attribute interacts with texrepeat above. Let texrepeat be N. The default value "false" means that the 2d texture is repeated N times over the (z-facing side of the) object. The value "true" means that the 2d texture is repeated N times over one spatial unit, regardless of object size.



<span class="at">emission</span>: <span class="at-val">real, "0"</span>  
Emission in OpenGL has the RGBA format, however we only provide a scalar setting. The RGB components of the OpenGL emission vector are the RGB components of the material color multiplied by the value specified here. The alpha component is 1.



<span class="at">specular</span>: <span class="at-val">real, "0.5"</span>  
Specularity in OpenGL has the RGBA format, however we only provide a scalar setting. The RGB components of the OpenGL specularity vector are all equal to the value specified here. The alpha component is 1. This value should be in the range \[0 1\].



<span class="at">shininess</span>: <span class="at-val">real, "0.5"</span>  
Shininess in OpenGL is a number between 0 and 128. The value given here is multiplied by 128 before passing it to OpenGL, so it should be in the range \[0 1\]. Larger values correspond to tighter specular highlight (thus reducing the overall amount of highlight but making it more salient visually). This interacts with the specularity setting; see OpenGL documentation for details.



<span class="at">reflectance</span>: <span class="at-val">real, "0"</span>  
This attribute should be in the range \[0 1\]. If the value is greater than 0, and the material is applied to a plane or a box geom, the renderer will simulate reflectance. The larger the value, the stronger the reflectance. For boxes, only the face in the direction of the local +Z axis is reflective. Simulating reflectance properly requires ray-tracing. This renderer uses the stencil buffer and suitable projections instead to approximate it. Only the first reflective geom in the model is rendered as such. This adds one extra rendering pass through all geoms, in addition to the extra rendering pass added by each shadow-casting light.



<span class="at">metallic</span>: <span class="at-val">real, "-1"</span>  
This attribute corresponds to uniform metallicity coefficient applied to the entire material. This attribute has no effect in MuJoCo's native renderer, but it can be useful when rendering scenes with a physically-based renderer. In this case, if a non-negative value is specified, this metallic value should be multiplied by the metallic texture sampled value to obtain the final metallicity of the material.



<span class="at">roughness</span>: <span class="at-val">real, "-1"</span>  
This attribute corresponds to uniform roughness coefficient applied to the entire material. This attribute has no effect in MuJoCo's native renderer, but it can be useful when rendering scenes with a physically-based renderer. In this case, if a non-negative value is specified, this roughness value should be multiplied by the roughness texture sampled value to obtain the final roughness of the material.



<span class="at">rgba</span>: <span class="at-val">real(4), "1 1 1 1"</span>  
Color and transparency of the material. All components should be in the range \[0 1\]. Note that the texture color (if assigned) and the color specified here are multiplied component-wise. Thus the default value of "1 1 1 1" has the effect of leaving the texture unchanged. When the material is applied to a model element which defines its own local rgba attribute, the local definition has precedence. Note that this "local" definition could in fact come from a defaults class. The remaining material properties always apply.


##### <span class="el-prefix">material/</span> ⁠ **layer** ​

If multiple textures are needed to specify the appearance of a material, the [texture](XMLreference.md) attribute cannot be used, and <span class="el">layer</span> child elements must be used instead. Specifying both the <span class="at">texture</span> attribute and <span class="el">layer</span> child elements is an error.


<span class="at">texture</span>: <span class="at-val">string, required</span>  
Name of the texture, like the [texture](XMLreference.md) attribute.



<span class="at">role</span>: <span class="at-val">string, required</span>  
Role of the texture. The valid values, expected number of channels, and the role semantics are:

| value | channels | description |
|----|----|----|
| <span class="at">rgb</span> | 3 | base color / albedo \[red, green, blue\] |
| <span class="at">normal</span> | 3 | bump map (surface normals) |
| <span class="at">occlusion</span> | 1 | ambient occlusion |
| <span class="at">roughness</span> | 1 | roughness |
| <span class="at">metallic</span> | 1 | metallicity |
| <span class="at">opacity</span> | 1 | opacity (alpha channel) |
| <span class="at">emissive</span> | 4 | RGB light emission intensity, exposure weight in 4th channel |
| <span class="at">orm</span> | 3 | packed 3 channel \[occlusion, roughness, metallic\] |
| <span class="at">rgba</span> | 4 | packed 4 channel \[red, green, blue, alpha\] |


#### <span class="el-prefix">asset/</span> ⁠ **model** ​

This element specifies other MJCF models which may be used for [attachment](XMLreference.md) in the current model.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the sub-model, used for referencing in [attach](XMLreference.md). If unspecified, the [model name](XMLreference.md) is used.



<span class="at">file</span>: <span class="at-val">string, required</span>  
The file from which the sub-model will be loaded. Note that the sub-model must be a valid MJCF model.



<span class="at">content_type</span> <span class="at-val">string, optional</span>  
The file type to be loaded into a model. Currently only text/xml is supported.


### **(world)body** `sync`

This element is used to construct the [kinematic tree](modeling.md) via nesting. The element <span class="el">worldbody</span> is used for the top-level body, while the element <span class="el">body</span> is used for all other bodies. The top-level body is a restricted type of body: it cannot have child elements [inertial](XMLreference.md) and [joint](XMLreference.md), and also cannot have any attributes. It corresponds to the origin of the world frame, within which the rest of the kinematic tree is defined. Its body name is automatically defined as "world".


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the body.



<span class="at">childclass</span>: <span class="at-val">string, optional</span>  
If this attribute is present, all descendant elements that admit a defaults class will use the class specified here, unless they specify their own class or another body or frame with a childclass attribute is encountered along the chain of nested bodies and frames. Recall [Default settings](modeling.md).



<span class="at">mocap</span>: <span class="at-val">\[false, true\], "false"</span>  
If this attribute is "true", the body is labeled as a mocap body. This is allowed only for bodies that are children of the world body and have no joints. Such bodies are fixed from the viewpoint of the dynamics, but nevertheless the forward kinematics set their position and orientation from the fields `mjData.mocap_{pos,quat}` at each time step. The size of these arrays is adjusted by the compiler so as to match the number of mocap bodies in the model. This mechanism can be used to stream motion capture data into the simulation. Mocap bodies can also be moved via mouse perturbations in the interactive visualizer, even in dynamic simulation mode. This can be useful for creating props with adjustable position and orientation. Mocap bodies are the weld root of their own kinematic subtree rather than being welded to the world: their children receive standard parent-child collision filtering, they do not generate contacts with static geometry, and contact with a mocap body wakes [sleeping](computation/index.md) bodies. See [mocap bodies](modeling.md) for more details.



<span class="at">pos</span>: <span class="at-val">real(3), optional</span>  
The 3D position of the body frame, in the parent coordinate frame. If undefined it defaults to (0,0,0).







<span class="at">quat</span>, <span class="at">axisangle</span>, <span class="at">xyaxes</span>, <span class="at">zaxis</span>, <span class="at">euler</span>  
See [Frame orientations](modeling.md).







<span class="at">gravcomp</span>: <span class="at-val">real, "0"</span>  
Gravity compensation force, specified as fraction of body weight. This attribute creates an upwards force applied to the body's center of mass, countering the force of gravity. As an example, a value of `1` creates an upward force equal to the body's weight and compensates for gravity exactly. Values greater than `1` will create a net upwards force or buoyancy effect.



<span class="at">sleep</span>: <span class="at-val">\[auto, never, allowed, init\], "auto"</span>  
[Sleep](computation/index.md) policy for the tree under this body. This attribute is only supported by moving bodies which are the root of a kinematic [tree](overview.md). For the default <span class="at-val">auto</span>, the compiler will set the sleep policy as follows:

- A tree which is affected by actuators is not allowed to sleep (overridable).
- Trees which are connected by tendons which have non-zero stiffness and damping are not allowed to sleep (overridable).
- Trees which are connected by tendons which connect more than two trees are not allowed to sleep (not overridable).
- Constraint-free [flexes](overview.md) are not allowed to sleep (not overridable).
- All other trees are allowed to sleep (overridable).

The policies <span class="at-val">never</span> and <span class="at-val">allowed</span> constitute user overrides of the automatic compiler policy.

The <span class="at-val">init</span> sleep policy can only be specified by the user and means "initialize this tree as asleep". This policy is implemented in *mj_resetData* and *mj_makeData* and only applies to the default configuration. If a [keyframe](XMLreference.md) changes the configuration of (or assigns nonzero velocity to) a sleeping tree, it will be woken up. This policy is useful for very large models where waiting for the automatic sleeping mechanism to kick in can be expensive. Trees initialized as sleeping can be placed in unstable configurations like deep penetration or in mid-air, but will only move when woken up. Also note that this policy can fail. For example if a tree marked as sleep="init" is in contact with a tree not marked as such (i.e., they are in the same [island](computation/index.md)) then it is impossible to put the tree to sleep; for such [models](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/sleep/init_island_fail.xml) a warning is issued and the trees which could not be slept start awake.

See [implementation notes](programming/simulation.md) for more details.



<span class="at">simple</span>: <span class="at-val">\[false, auto\], "auto"</span>  
Controls the *simple body* optimization. When a body qualifies as "simple", its inertial matrix block in the mass matrix is diagonal, representing independent translational and rotational degrees of freedom. The optimization omits storing of the zero-valued off-diagonal entries, reducing memory footprint and computation.

A body qualifies for this optimization if it satisfies all of the following:

- **Inertial frame alignment**: The body's inertial frame coincides with its body frame.
- **Kinematic root**: The body's parent is either the world body or a static body.
- **Leaf body**: The body is a leaf node in the kinematic tree (it has no child bodies).
- **Origin-centered joints**: All joints belonging to this body must reside at the body's origin.
- **Aligned joint axes**: Any hinge or slide joint axes must be aligned with the local coordinate axes, and at most one joint with rotational degrees of freedom (hinge or ball) is permitted.
- **No inertia-bearing tendons**: The body must not contain sites or geoms used as wrap objects by any tendon that has non-zero [armature](XMLreference.md).

Setting this attribute to <span class="at-val">false</span> disables the optimization for this body. This is necessary for domain randomization workflows where model parameters (such as joint/inertial offsets or angles) are perturbed dynamically during simulation and updated via *mj_setConst*. Because a body compiled with the simple optimization active cannot dynamically lose its simple state at runtime (which would require reallocation of sparse matrix structures), any runtime parameter change that violates the simple conditions will trigger a validation error unless `simple="false"` was explicitly declared in the XML.



<span class="at">fuse</span>: <span class="at-val">\[false, auto\], "auto"</span>  
Whether this body can be fused with its parent when static bodies are fused, by the [fusestatic](XMLreference.md) compiler option or by *mjs_fuseStatic*. With the default <span class="at-val">auto</span> a static body is fused unless one of the conditions listed there prevents it. Setting this attribute to <span class="at-val">false</span> keeps the body.



<span class="at">user</span>: <span class="at-val">real(nbody_user), "0 0 ..."</span>  
See [User parameters](modeling.md).


#### <span class="el-prefix">body/</span> ⁠ **inertial** `dot`

This element specifies the mass and inertial properties of the body. If this element is not included in a given body, the inertial properties are inferred from the geoms attached to the body. A saved model has this element where it was written; the inferred properties are saved with it as well when [saveinertial](XMLreference.md) is set, and in a model saved with the values which compilation made ([savecompiled](XMLreference.md), the default) also when [settotalmass](XMLreference.md) scaled them or the saved file would not infer them again. The inertial frame is such that its center coincides with the center of mass of the body, and its axes coincide with the principal axes of inertia of the body. Thus the inertia matrix is diagonal in this frame.


<span class="at">pos</span>: <span class="at-val">real(3), required</span>  
Position of the inertial frame. This attribute is required even when the inertial properties can be inferred from geoms. This is because the presence of the <span class="el">inertial</span> element itself disables the automatic inference mechanism.







<span class="at">quat</span>, <span class="at">axisangle</span>, <span class="at">xyaxes</span>, <span class="at">zaxis</span>, <span class="at">euler</span>  
Orientation of the inertial frame. See [Frame orientations](modeling.md).







<span class="at">mass</span>: <span class="at-val">real, required</span>  
Mass of the body. Negative values are not allowed. MuJoCo requires the inertia matrix in generalized coordinates to be positive-definite, which can sometimes be achieved even if some bodies have zero mass. In general however there is no reason to use massless bodies. Such bodies are often used in other engines to bypass the limitation that joints cannot be combined, or to attach sensors and cameras. In MuJoCo primitive joint types can be combined, and we have sites which are a more efficient attachment mechanism.



<span class="at">diaginertia</span>: <span class="at-val">real(3), optional</span>  
Diagonal inertia matrix, expressing the body inertia relative to the inertial frame. If this attribute is omitted, the next attribute becomes required.



<span class="at">fullinertia</span>: <span class="at-val">real(6), optional</span>  
Full inertia matrix M. Since M is 3-by-3 and symmetric, it is specified using only 6 numbers in the following order: M(1,1), M(2,2), M(3,3), M(1,2), M(1,3), M(2,3). The compiler computes the eigenvalue decomposition of M and sets the frame orientation and diagonal inertia accordingly. If non-positive eigenvalues are encountered (i.e., if M is not positive definite) a compile error is generated, unless [boundinertia](XMLreference.md) is positive, in which case the eigenvalues are bounded below by it.


#### <span class="el-prefix">body/</span> ⁠ **joint** ​

This element creates a joint. As explained in [Kinematic tree](modeling.md), a joint creates motion degrees of freedom between the body where it is defined and the body's parent. If multiple joints are defined in the same body, the corresponding spatial transformations (of the body frame relative to the parent frame) are applied in order. If no joints are defined, the body is welded to its parent. Joints cannot be defined in the world body. At runtime the positions and orientations of all joints defined in the model are stored in the vector `mjData.qpos`, in the order in which they appear in the kinematic tree. The linear and angular velocities are stored in the vector `mjData.qvel`. These two vectors have different dimensionality when free or ball joints are used, because such joints represent rotations as unit quaternions.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the joint.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">type</span>: <span class="at-val">\[free, ball, slide, hinge\], "hinge"</span>  
Type of the joint. The keywords have the following meaning: The **free** type creates a free "joint" with three translational degrees of freedom followed by three rotational degrees of freedom. In other words it makes the body floating. The rotation is represented as a unit quaternion. This joint type is only allowed in bodies that are children of the world body. No other joints can be defined in the body if a free joint is defined. Unlike the remaining joint types, free joints do not have a position within the body frame. Instead the joint position is assumed to coincide with the center of the body frame. Thus at runtime the position and orientation data of the free joint correspond to the global position and orientation of the body frame. Free joints cannot have limits.

The **ball** type creates a ball joint with three rotational degrees of freedom. The rotation is represented as a unit quaternion. The quaternion (1,0,0,0) corresponds to the initial configuration in which the model is defined. Any other quaternion is interpreted as a 3D rotation relative to this initial configuration. The rotation is around the point defined by the [pos](XMLreference.md) attribute. If a body has a ball joint, it cannot have other rotational joints (ball or hinge). Combining ball joints with slide joints in the same body is allowed.

The **slide** type creates a sliding or prismatic joint with one translational degree of freedom. Such joints are defined by a position and a sliding direction. For simulation purposes only the direction is needed; the joint position is used for rendering purposes.

The **hinge** type creates a hinge joint with one rotational degree of freedom. The rotation takes place around a specified axis through a specified position. This is the most common type of joint and is therefore the default. Most models contain only hinge and free joints.



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
Integer group to which the joint belongs. This attribute can be used for custom tags. It is also used by the visualizer to enable and disable the rendering of entire groups of joints.



<span class="at">pos</span>: <span class="at-val">real(3), "0 0 0"</span>  
Position of the joint, specified in the frame of the body where the joint is defined. For free joints this attribute is ignored.



<span class="at">axis</span>: <span class="at-val">real(3), "0 0 1"</span>  
This attribute specifies the axis of rotation for hinge joints and the direction of translation for slide joints. It is ignored for free and ball joints. The vector specified here is automatically normalized to unit length as long as its length is greater than 10E-14; otherwise a compile error is generated.



<span class="at">springdamper</span>: <span class="at-val">real(2), "0 0"</span>  
When both numbers are positive, the compiler will override any stiffness and damping values specified with the attributes below, and will instead set them automatically so that the resulting mass-spring-damper for this joint has the desired time constant (first value) and damping ratio (second value). This is done by taking into account the joint inertia in the model reference configuration. Note that the format is the same as the solref parameter of the constraint solver.




<span class="at">solreflimit</span>, <span class="at">solimplimit</span>  
Constraint solver parameters for simulating joint limits. See [Solver parameters](modeling.md).





<span class="at">solreffriction</span>, <span class="at">solimpfriction</span>  
Constraint solver parameters for simulating dry friction. See also [Friction](modeling.md).




<span class="at">stiffness</span>: <span class="at-val">real, "0 0 0"</span>  
Joint stiffness coefficients $`a, b, c`$. A positive $`a`$ produces the standard restorative linear spring force $`f = -a x`$, where $`x`$ is the joint displacement from equilibrium given by [springref](XMLreference.md).

If the optional second and third components are set, they define a nonlinear polynomial spring force $`f(x) = -(a x + b x^2 + c x^3)`$. See [Polynomial forces](computation/index.md) for details.



<span class="at">range</span>: <span class="at-val">real(2), "0 0"</span>  
The joint limits. Limits can be imposed on all joint types except for free joints. For hinge and ball joints, the range is specified in degrees or radians depending on the angle attribute of [compiler](XMLreference.md). For ball joints, the limit is imposed on the angle of rotation (relative to the reference configuration) regardless of the axis of rotation. Only the second range parameter is used for ball joints; the first range parameter should be set to 0. See the [Limit](computation/index.md) section in the Computation chapter for more information. <br/> Setting this attribute without specifying <span class="at">limited</span> is an error if <span class="at">autolimits</span> is "false" in [compiler](XMLreference.md).



<span class="at">limited</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
This attribute specifies if the joint has limits. It interacts with the [range](XMLreference.md) attribute. If this attribute is "false", joint limits are disabled. If this attribute is "true", joint limits are enabled. If this attribute is "auto", and <span class="at">autolimits</span> is set in [compiler](XMLreference.md), joint limits will be enabled if range is defined.



<span class="at">actuatorfrcrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping total actuator forces acting on this joint. See [Force limits](modeling.md) for details; to limit several commands of one physical actuator, prefer a single multi-input actuator such as [pid](XMLreference.md) with [forcerange](XMLreference.md). It is available only for scalar joints (hinge and slider) and ignored for ball and free joints. <br/> The compiler expects the first value to be smaller than the second value. <br/> Setting this attribute without specifying <span class="at">actuatorfrclimited</span> is an error if <span class="at">compiler-autolimits</span> is "false".



<span class="at">actuatorfrclimited</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
This attribute specifies whether actuator forces acting on the joint should be clamped. See [Force limits](modeling.md) for details. It is available only for scalar joints (hinge and slider) and ignored for ball and free joints. <br/> This attribute interacts with the [actuatorfrcrange](XMLreference.md) attribute. If this attribute is "false", actuator force clamping is disabled. If it is "true", actuator force clamping is enabled. If this attribute is "auto", and <span class="at">autolimits</span> is set in [compiler](XMLreference.md), actuator force clamping will be enabled if <span class="at">actuatorfrcrange</span> is defined.



<span class="at">actuatorgravcomp</span>: <span class="at-val">\[false, true\], "false"</span>  
If this flag is enabled, gravity compensation applied to this joint is added to actuator forces (`mjData.qfrc_actuator`) rather than passive forces (`mjData.qfrc_passive`). Notionally, this means that gravity compensation is the result of a control system rather than natural buoyancy. In practice, enabling this flag is useful when joint-level actuator force clamping is used. In this case, the total actuation force applied on a joint, including gravity compensation, is guaranteed to not exceed the specified limits. See [Force limits](modeling.md) and [actuatorfrcrange](XMLreference.md) for more details on this type of force limit.



<span class="at">margin</span>: <span class="at-val">real, "0"</span>  
The distance threshold below which limits become active. Recall that the [Constraint solver](computation/index.md) normally generates forces as soon as a constraint becomes active, even if the margin parameter makes that happen at a distance. This attribute together with solreflimit and solimplimit can be used to model a soft joint limit.



<span class="at">ref</span>: <span class="at-val">real, "0"</span>  
The reference position or angle of the joint. This attribute is only used for slide and hinge joints. It defines the joint value corresponding to the initial model configuration. Note that the initial configuration itself is unmodified, only the value of the joint at this configuration. The amount of spatial transformation that the joint applies at runtime equals the current joint value stored in `mjData.qpos` minus this reference value stored in `mjModel.qpos0`. The meaning of these vectors is discussed in the [Kinematic tree](overview.md) section in the Overview chapter.



<span class="at">springref</span>: <span class="at-val">real, "0"</span>  
The joint position or angle in which the joint spring (if any) achieves equilibrium. Similar to the vector mjModel.qpos0 which stores all joint reference values specified with the ref attribute above, all spring reference values specified with this attribute are stored in the vector mjModel.qpos_spring. The model configuration corresponding to mjModel.qpos_spring is also used to compute the spring reference lengths of all tendons, stored in mjModel.tendon_lengthspring. This is because [tendons](XMLreference.md) can also have springs.


[<img src="https://www.gstatic.com/mujoco/model/plastic/wire.webp" class="align-right" style="width:40.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/model/plastic/wire.xml)


<span class="at">springyield</span>: <span class="at-val">real, "0"</span>  
Elastic yield threshold for the joint spring. Available on slide, hinge, and ball joints (not supported on free joints). For hinge and ball joints, the threshold is specified in degrees or radians depending on the <span class="at">angle</span> attribute of [compiler](XMLreference.md). When positive, the joint spring reference is allocated in the mutable state vector `mjData.plastic` at offset `mjModel.jnt_plasticadr[j]` (1 entry for slide/hinge, 4 quaternion entries for ball, initialized from `mjModel.qpos_spring`) and shifts permanently whenever the spring displacement exceeds `springyield` (ideal elasto-plasticity). When `0` (default), plasticity is disabled (`mjModel.jnt_plasticadr[j] == -1`) and the spring is purely elastic; setting `mjModel.jnt_springyield[j] = 0` at runtime on an already-plastic joint (`jnt_plasticadr[j] >= 0`) corresponds to zero yield threshold (full plastic slip). See [model/plastic/](https://github.com/google-deepmind/mujoco/tree/main/model/plastic/) for example models.


[<img src="images/XMLreference/armature.gif" class="only-light only-lightalign-right" style="width:40.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/armature_equivalence.xml)

[<img src="images/XMLreference/armature_dark.gif" class="only-dark only-darkalign-right" style="width:40.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/armature_equivalence.xml)


<span class="at">armature</span>: <span class="at-val">real, "0"</span>  
Additional inertia associated with movement of the joint that is not due to body mass. This added inertia is usually due to a rotor (a.k.a [armature](https://en.wikipedia.org/wiki/Armature_(electrical))) spinning faster than the joint itself due to a geared transmission. In the illustration, we compare (*left*) a 2-dof system with an armature body (purple box), coupled with a gear ratio of $`3`$ to the pendulum using a [joint equality](XMLreference.md) constraint, and (*right*) a simple 1-dof pendulum with an equivalent <span class="at">armature</span>. Because the gear ratio appears twice, multiplying both forces and lengths, the effect is known as "reflected inertia" and the equivalent value is the inertia of the spinning body multiplied by the *square of the gear ratio*, in this case $`9=3^2`$. The value applies to all degrees of freedom created by this joint.

Besides increasing the realism of joints with geared transmission, positive <span class="at">armature</span> significantly improves simulation stability, even for small values, and is a recommended possible fix when encountering stability issues.



<span class="at">damping</span>: <span class="at-val">real, "0 0 0"</span>  
Damping coefficients $`a, b, c`$. A positive $`a`$ produces the standard dissipative linear damping force $`f(v) = -a v`$, where $`v`$ is the joint velocity. Despite its simplicity, larger damping values can make numerical integrators unstable, which is why our Euler integrator handles damping implicitly. See [Integration](computation/index.md) in the Computation chapter.

If the optional second and third components are set, they define a nonlinear polynomial damping force $`f(v) = -(a v + b v |v| + c v^3)`$. Note the anti-symmetrization of the quadratic term, ensuring that the force is an odd function of velocity. See [Polynomial forces](computation/index.md) for details.



<span class="at">frictionloss</span>: <span class="at-val">real, "0"</span>  
Friction loss due to dry friction. This value is the same for all degrees of freedom created by this joint. Semantically friction loss does not make sense for free joints, but the compiler allows it. To enable friction loss, set this attribute to a positive value.



<span class="at">user</span>: <span class="at-val">real(njnt_user), "0 0 ..."</span>  
See [User parameters](modeling.md).


#### <span class="el-prefix">body/</span> ⁠ **freejoint** ​

This element creates a free joint whose only attributes are <span class="at">name</span> and <span class="at">group</span>. The <span class="el">freejoint</span> element is an XML shortcut for

``` xml
<joint type="free" stiffness="0" damping="0" frictionloss="0" armature="0"/>
```

While this joint can evidently be created with the [joint](XMLreference.md) element, default joint settings could affect it. This is usually undesirable as physical free bodies do not have nonzero stiffness, damping, friction or armature. To avoid this complication, the <span class="el">freejoint</span> element was introduced, ensuring joint defaults are *not inherited*. In a model which is saved [as it was compiled](XMLreference.md) it appears as a regular joint of type <span class="at">free</span>.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the joint.



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
Integer group to which the joint belongs. This attribute can be used for custom tags. It is also used by the visualizer to enable and disable the rendering of entire groups of joints.



<span class="at">align</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
When set to <span class="at-val">true</span>, the body frame and free joint will automatically be aligned with inertial frame. When set to <span class="at-val">false</span>, no alignment will occur. When set to <span class="at-val">auto</span>, the compiler's [alignfree](XMLreference.md) global attribute will be respected.

Inertial frame alignment is an optimization only applies to bodies with a free joint and no child bodies ("simple free bodies"). The alignment diagonalizes the 6x6 inertia matrix and minimizes bias forces, leading to faster and more stable simulation. While this behaviour is a strict improvement, it modifies the semantics of the free joint, making `qpos` and `qvel` values saved in older versions (for example, in [keyframes](XMLreference.md)) invalid.

Note that when the values which compilation made are saved ([savecompiled](XMLreference.md)), the <span class="at">align</span> attribute is not saved. Instead, the pose of simple free bodies and their children will be modified such that the body frame and inertial frame are aligned.


#### <span class="el-prefix">body/</span> ⁠ **geom** ​

This element creates a geom, and attaches it rigidly to the body within which the geom is defined. Multiple geoms can be attached to the same body. At runtime they determine the appearance and collision properties of the body. At compile time they can also determine the inertial properties of the body, depending on the presence of the [inertial](XMLreference.md) element and the setting of the inertiafromgeom attribute of [compiler](XMLreference.md). This is done by summing the masses and inertias of all geoms attached to the body with geom group in the range specified by the inertiagrouprange attribute of [compiler](XMLreference.md). The geom masses and inertias are computed using the geom shape, a specified density or a geom mass which implies a density, and the assumption of uniform density.

Geoms are not strictly required for physics simulation. One can create and simulate a model that only has bodies and joints. Such a model can even be visualized, using equivalent inertia boxes to represent bodies. Only contact forces would be missing from such a simulation. We do not recommend using such models, but knowing that this is possible helps clarify the role of bodies and geoms in MuJoCo.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the geom.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">type</span>: <span class="at-val">\[plane, hfield, sphere, capsule, ellipsoid, cylinder, box, mesh, sdf\], "sphere"</span>  
Type of geometric shape. The keywords have the following meaning: The **plane** type defines a surface which is infinite for collision detection purposes. It can only be attached to the world body or static children of the world. The plane passes through a point specified via the pos attribute. It is normal to the Z axis of the geom's local frame. The +Z direction corresponds to empty space. Thus the position and orientation defaults of (0,0,0) and (1,0,0,0) would create a ground plane at Z=0 elevation, with +Z being the vertical direction in the world (which is MuJoCo's convention). Since the plane is infinite, it could have been defined using any other point in the plane. The specified position however has additional meaning with regard to rendering. If either of the first two size parameters are positive, the plane is rendered as a rectangle of finite size (in the positive dimensions). This rectangle is centered at the specified position. Three size parameters are required. The first two specify the half- size of the rectangle along the X and Y axes. The third size parameter is unusual: it specifies the spacing between the grid subdivisions of the plane for rendering purposes. The subdivisions are revealed in wireframe rendering mode, but in general they should not be used to paint a grid over the ground plane (textures should be used for that purpose). Instead their role is to improve lighting and shadows, similar to the subdivisions used to render boxes. When planes are viewed from the back, the are automatically made semi-transparent. Planes and the +Z faces of boxes are the only surfaces that can show reflections, if the [material](XMLreference.md) applied to the geom has positive reflection. To render an infinite plane, set the first two size parameters to zero.

The **hfield** type defines a height field geom. The geom must reference the desired height field asset with the hfield attribute below. The position and orientation of the geom set the position and orientation of the height field. The size of the geom is ignored, and the size parameters of the height field asset are used instead. See the description of the [hfield](XMLreference.md) element. Similar to planes, height field geoms can only be attached to the world body or to static children of the world.

The **sphere** type defines a sphere. This and the next four types correspond to built-in geometric primitives. These primitives are treated as analytic surfaces for collision detection purposes, in many cases relying on custom pair- wise collision routines. Models including only planes, spheres, capsules and boxes are the most efficient in terms of collision detection. Other geom types invoke the general-purpose convex collider. The sphere is centered at the geom's position. Only one size parameter is used, specifying the radius of the sphere. Rendering of geometric primitives is done with automatically generated meshes whose density can be adjusted via [quality](XMLreference.md). The sphere mesh is triangulated along the lines of latitude and longitude, with the Z axis passing through the north and south pole. This can be useful in wireframe mode for visualizing frame orientation.

The **capsule** type defines a capsule, which is a cylinder capped with two half-spheres. It is oriented along the Z axis of the geom's frame. When the geom frame is specified in the usual way, two size parameters are required: the radius of the capsule followed by the half-height of the cylinder part. However capsules as well as cylinders can also be thought of as connectors, allowing an alternative specification with the fromto attribute below. In that case only one size parameter is required, namely the radius of the capsule.

The **ellipsoid** type defines a ellipsoid. This is a sphere scaled separately along the X, Y and Z axes of the local frame. It requires three size parameters, corresponding to the three radii. Note that even though ellipsoids are smooth, their collisions are handled via the general-purpose convex collider. The only exception are plane-ellipsoid collisions which are computed analytically.

The **cylinder** type defines a cylinder. It requires two size parameters: the radius and half-height of the cylinder. The cylinder is oriented along the Z axis of the geom's frame. It can alternatively be specified with the fromto attribute below.

The **box** type defines a box. Three size parameters are required, corresponding to the half-sizes of the box along the X, Y and Z axes of the geom's frame. Note that box-box collisions can generate up to 8 contact points.

The **mesh** type defines a mesh. The geom must reference the desired mesh asset with the mesh attribute. Note that mesh assets can also be referenced from other geom types, causing primitive shapes to be fitted; see below. The size is determined by the mesh asset and the geom size parameters are ignored. Unlike all other geoms, the position and orientation of mesh geoms after compilation do not equal the settings of the corresponding attributes here. Instead they are offset by the translation and rotation that were needed to center and align the mesh asset in its own coordinate frame. Recall the discussion of centering and alignment in the [mesh](XMLreference.md) element.

The **sdf** type defines a signed distance field (SDF, also referred to as signed distance function). In order to visualize the SDF, a custom mesh must be specified using the [mesh/plugin](XMLreference.md) attribute. See the [model/plugin/sdf/](https://github.com/google-deepmind/mujoco/tree/main/model/plugin/sdf) directory for example models with SDF geometries. For more details regarding SDF plugins, see the [Extensions chapter](programming/extension.md).



<span class="at">contype</span>: <span class="at-val">int, "1"</span>  
This attribute and the next specify 32-bit integer bitmasks used for contact filtering of dynamically generated contact pairs. See [Collision detection](computation/index.md) in the Computation chapter. Two geoms can collide if the contype of one geom is compatible with the conaffinity of the other geom or vice versa. Compatible means that the two bitmasks have a common bit set to 1.



<span class="at">conaffinity</span>: <span class="at-val">int, "1"</span>  
Bitmask for contact filtering; see contype above.



<span class="at">condim</span>: <span class="at-val">int, "3"</span>  
The dimensionality of the contact space for a dynamically generated contact pair is set to the maximum of the condim values of the two participating geoms. See [Contact](computation/index.md) in the Computation chapter. The allowed values and their meaning are:

| condim | Description |
|----|----|
| 1 | Frictionless contact. |
| 3 | Regular frictional contact, opposing slip in the tangent plane. |
| 4 | Frictional contact, opposing slip in the tangent plane and rotation around the contact normal. This is useful for modeling soft contacts (independent of contact penetration). |
| 6 | Frictional contact, opposing slip in the tangent plane, rotation around the contact normal and rotation around the two axes of the tangent plane. The latter frictional effects are useful for preventing objects from indefinite rolling. |



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
This attribute specifies an integer group to which the geom belongs. The only effect on the physics is at compile time, when body masses and inertias are inferred from geoms selected based on their group; see inertiagrouprange attribute of [compiler](XMLreference.md). At runtime this attribute is used by the visualizer to enable and disable the rendering of entire geom groups. By default, groups 0, 1 and 2 are visible, while all other groups are invisible. The group attribute can also be used as a tag for custom computations.



<span class="at">priority</span>: <span class="at-val">int, "0"</span>  
The geom priority determines how the properties of two colliding geoms are combined to form the properties of the contact. This interacts with the solmix attribute. See [Contact parameters](modeling.md).



<span class="at">size</span>: <span class="at-val">real(3), "0 0 0"</span>  
Geom size parameters. The number of required parameters and their meaning depends on the geom type as documented under the type attribute. Here we only provide a summary. All required size parameters must be positive; the internal defaults correspond to invalid settings. Note that when a non-mesh geom type references a mesh, a geometric primitive of that type is fitted to the mesh. In that case the sizes are obtained from the mesh, and the geom size parameters are ignored. Thus the number and description of required size parameters in the table below only apply to geoms that do not reference meshes.

| Type | Number | Description |
|----|----|----|
| plane | 3 | X half-size; Y half-size; spacing between square grid lines for rendering. If either the X or Y half-size is 0, the plane is rendered as infinite in the dimension(s) with 0 size. |
| hfield | 0 | The geom sizes are ignored and the height field sizes are used instead. |
| sphere | 1 | Radius of the sphere. |
| capsule | 1 or 2 | Radius of the capsule; half-length of the cylinder part when not using the <span class="at">fromto</span> specification. |
| ellipsoid | 3 | X radius; Y radius; Z radius. |
| cylinder | 1 or 2 | Radius of the cylinder; half-length of the cylinder when not using the <span class="at">fromto</span> specification. |
| box | 3 | X half-size; Y half-size; Z half-size. |
| mesh | 0 | The geom sizes are ignored and the mesh sizes are used instead. |



<span class="at">material</span>: <span class="at-val">string, optional</span>  
If specified, this attribute applies a material to the geom. Otherwise, if unspecified and the type of the geom is a **mesh** the compiler will apply the mesh asset [material](XMLreference.md) if present.

The material determines the visual properties of the geom. The only exception is color: if the rgba attribute below is different from its internal default, it takes precedence while the remaining material properties are still applied. Note that if the same material is referenced from multiple geoms (as well as sites and tendons) and the user changes some of its properties at runtime, these changes will take effect immediately for all model elements referencing the material. This is because the compiler saves the material and its properties as a separate element in mjModel, and the elements using this material only keep a reference to it.



<span class="at">rgba</span>: <span class="at-val">real(4), "0.5 0.5 0.5 1"</span>  
Instead of creating material assets and referencing them, this attribute can be used to set color and transparency only. This is not as flexible as the material mechanism, but is more convenient and is often sufficient. If the value of this attribute is different from the internal default, it takes precedence over the material.



<span class="at">castshadow</span>: <span class="at-val">\[false, true\], "true"</span>  
If this attribute is "true", the geom casts shadows when illuminated by shadow-casting lights (those with [castshadow](XMLreference.md) set to "true"). Setting this to "false" disables shadow casting for this geom while still allowing it to receive shadows and be lit normally.



<span class="at">friction</span>: <span class="at-val">real(3), "1 0.005 0.0001"</span>  
Contact friction parameters for dynamically generated contact pairs. The first number is the sliding friction, acting along both axes of the tangent plane. The second number is the torsional friction, acting around the contact normal. The third number is the rolling friction, acting around both axes of the tangent plane. The friction parameters for the contact pair are combined depending on the solmix and priority attributes, as explained in [Contact parameters](modeling.md). See the general [Contact](computation/index.md) section for descriptions of the semantics of this attribute.



<span class="at">mass</span>: <span class="at-val">real, optional</span>  
If this attribute is specified, the density attribute below is ignored and the geom density is computed from the given mass, using the geom shape and the assumption of uniform density. The computed density is then used to obtain the geom inertia. Recall that the geom mass and inertia are only used during compilation, to infer the body mass and inertia if necessary. At runtime only the body inertial properties affect the simulation; the geom mass and inertia are not saved in mjModel.



<span class="at">density</span>: <span class="at-val">real, "1000"</span>  
Material density used to compute the geom mass and inertia. The computation is based on the geom shape and the assumption of uniform density. The internal default of 1000 is the density of water in SI units. This attribute is used only when the mass attribute above is unspecified. If <span class="title-ref">shellinertia</span> is "false" (the default), density has semantics of mass/volume; if "true", it has semantics of mass/area.



<span class="at">shellinertia</span> <span class="at-val">\[false, true\], "false"</span>  
If true, the geom's inertia is computed assuming that all the mass is concentrated on the surface. In this case <span class="at">density</span> is interpreted as surface rather than volumetric density. This attribute only applies to primitive geoms and is ignored for meshes. Surface inertia for meshes can be specified by setting the [asset/mesh/inertia](XMLreference.md) attribute to <span class="at-val">"shell"</span>.



<span class="at">solmix</span>: <span class="at-val">real, "1"</span>  
This attribute specifies the weight used for averaging of contact parameters, and interacts with the priority attribute. See [Contact parameters](modeling.md).




<span class="at">solref</span>, <span class="at">solimp</span>  
Constraint solver parameters for contact simulation. See [Solver parameters](modeling.md).




<span class="at">margin</span>: <span class="at-val">real, "0"</span>  
Geometric inflation of the geom surface for the purpose of contact force generation. When the distance between two geom surfaces is below `margin`, the contact is considered active and contact forces are generated. The constraint impedance can be a function of distance, as explained in [Solver parameters](modeling.md). The quantity this function is applied to is the distance between the two geoms minus the `margin`. See [margin and gap](computation/index.md).



<span class="at">gap</span>: <span class="at-val">real, "0"</span>  
Additional contact detection buffer beyond `margin`. When this value is positive, contacts are detected at distance `margin + gap` but forces are only generated at distance `margin`. Contacts with distance between `margin` and `margin + gap` are included in `mjData.contact` as inactive contacts (with `efc_address` = -1). These inactive contacts can be used for custom computations, for example by [adhesion](XMLreference.md) actuators which use contacts in the gap zone to generate adhesive forces without producing contact forces. See [margin and gap](computation/index.md).




PdSdrqhSiZA



<span class="at">surfacevel</span>: <span class="at-val">real(6), "0 0 0 0 0 0"</span>  
Velocity of the geom's surface as seen by contacts, given as a velocity field $`\sigma(x)`$ with two components: a constant velocity $`v`$ (first three numbers) and a rotational field with angular velocity $`\omega`$ (last three numbers) about the geom frame origin $`p`$, both expressed in the geom frame:

``` math
\sigma(x) = v + \omega \times (x - p)
```

A contact with the geom observes the surface moving along this field, with the velocity projected onto the contact's tangent plane: no normal velocity is imparted. When <span class="at">condim</span> is 4 or larger, the angular velocity $`\omega`$ also drives torsional friction. <span class="at">surfacevel</span> models surfaces that move while the geom itself does not: conveyor belts, treadmills and turntables can be constructed with no degrees of freedom. Friction drives touching bodies along the motion of the surface: objects placed on a conveyor are transported at belt speed, and a turntable (angular surface velocity about the cylinder axis) imparts tangential velocity that grows with radius. Surface velocities of two touching geoms compose as relative velocity, and compose correctly with body motion (a conveyor mounted on a moving vehicle works as expected). Note that this attribute describes the geom's *entire* surface: a box with constant `surfacevel` moves all six faces. When contact points are visualized, a contact with a moving surface additionally displays an arrow along the tangential surface velocity at the contact point. This attribute can be modified at runtime.



GioWwB36XHI



<span class="at">adhesion</span>: <span class="at-val">real, "0"</span>  
Adhesive force of contacts with this geom, in units of force. Geometrically, the friction cone is translated down along the normal so that the force origin lies strictly inside it: each contact can pull with up to `adhesion` before breaking, and the friction budget becomes $`\mu(f_N + \text{adhesion})`$. Contacts resist sliding even under zero normal force, the defining property of cohesive materials. This is useful for sticky materials (tape, gecko feet, tacky rubber) and as a physical stabilizer for grasping. The adhesion of a contact is the sum of the values of the two contacting geoms, or the value of the higher-[priority](XMLreference.md) geom if priorities differ; an explicit contact [pair](XMLreference.md) overrides both. Note that adhesion is *per contact*: a box face resting on a plane generates four contact points and therefore four times the pull-off force of a single-point contact. To let adhesion act across a small separation (attraction at a distance), set [gap](XMLreference.md) to the desired interaction range. This can be used to model magnets. Resting penetration is unaffected by adhesion (the compression behavior of the contact is unchanged; only a tensile branch is added), and *mj_contactForce* reports the net interface force, whose normal component can be negative under tension. The underlying model is described in the [Computation chapter](computation/index.md). For adhesion as a *controlled* force — switched on and off like a vacuum gripper, dividing a total force between a body's contacts and pressing the bodies together — see the [adhesion actuator](XMLreference.md).


<span class="at">fromto</span>: <span class="at-val">real(6), optional</span>  
<figure class="align-right">
<img src="images/XMLreference/fromto.png" width="350" />
</figure>

This attribute can only be used with capsule, box, cylinder and ellipsoid geoms. It provides an alternative specification of the geom length as well as the frame position and orientation. The six numbers are the 3D coordinates of one point followed by the 3D coordinates of another point. The elongated part of the geom connects these two points, with the +Z axis of the geom's frame oriented from the first towards the second point, while in the perpendicular direction, the geom sizes are both equal to the first value of the <span class="at">size</span> attribute. The frame orientation is obtained with the same procedure as the <span class="at">zaxis</span> attribute described in [Frame orientations](modeling.md). The frame position is in the middle between the end points. If this attribute is specified, the remaining position and orientation-related attributes are ignored. The image on the right demonstrates use of <span class="at">fromto</span> with the four supported geoms, using identical Z values. The model is [here](_static/fromto.xml). Note that the <span class="at">fromto</span> semantics of *capsule* are unique: the two end points specify the segment around which the radius defines the capsule surface.



<span class="at">pos</span>: <span class="at-val">real(3), "0 0 0"</span>  
Position of the geom, specified in the frame of the body where the geom is defined.







<span class="at">quat</span>, <span class="at">axisangle</span>, <span class="at">xyaxes</span>, <span class="at">zaxis</span>, <span class="at">euler</span>  
Orientation of the geom frame. See [Frame orientations](modeling.md).







<span class="at">hfield</span>: <span class="at-val">string, optional</span>  
This attribute must be specified if and only if the geom type is "hfield". It references the height field asset to be instantiated at the position and orientation of the geom frame.



<span class="at">mesh</span>: <span class="at-val">string, optional</span>  
If the geom type is "mesh", this attribute is required. It references the mesh asset to be instantiated. This attribute can also be specified if the geom type corresponds to a geometric primitive, namely one of "sphere", "capsule", "cylinder", "ellipsoid", "box". In that case the primitive is automatically fitted to the mesh asset referenced here. The fitting procedure uses either the equivalent inertia box or the axis-aligned bounding box of the mesh, as determined by the attribute fitaabb of [compiler](XMLreference.md). The resulting size of the fitted geom is usually what one would expect, but if not, it can be further adjusted with the fitscale attribute below. In the compiled mjModel the geom is represented as a regular geom of the specified primitive type, and there is no reference to the mesh used for fitting.



<span class="at">fitscale</span>: <span class="at-val">real, "1"</span>  
This attribute is used only when a primitive geometric type is being fitted to a mesh asset. The scale specified here is relative to the output of the automated fitting procedure. The default value of 1 leaves the result unchanged, a value of 2 makes all sizes of the fitted geom two times larger.



<span class="at">fluidshape</span>: <span class="at-val">\[none, ellipsoid\], "none"</span>  
"ellipsoid" activates the geom-level fluid interaction model based on an ellipsoidal approximation of the geom shape. When active, the model based on [body inertia sizes](computation/fluid.md) is disabled for the body in which the geom is defined. See section on [ellipsoid-based](computation/fluid.md) fluid interaction model for details.



<span class="at">fluidcoef</span>: <span class="at-val">real(5), "0.5 0.25 1.5 1.0 1.0"</span>  
Dimensionless coefficients of fluid interaction model, as follows. See section on [ellipsoid-based](computation/fluid.md) fluid interaction model for details.


| Index | Description              | Symbol                    | Default |
|-------|--------------------------|---------------------------|---------|
| 0     | Blunt drag coefficient   | $`C_{D, \text{blunt}}`$   | 0.5     |
| 1     | Slender drag coefficient | $`C_{D, \text{slender}}`$ | 0.25    |
| 2     | Angular drag coefficient | $`C_{D, \text{angular}}`$ | 1.5     |
| 3     | Kutta lift coefficient   | $`C_K`$                   | 1.0     |
| 4     | Magnus lift coefficient  | $`C_M`$                   | 1.0     |


<span class="at">user</span>: <span class="at-val">real(nuser_geom), "0 0 ..."</span>  
See [User parameters](modeling.md).


##### <span class="el-prefix">geom/</span> ⁠ **plugin** `dot`

Associate this geom with an [engine plugin](programming/extension.md). Either <span class="at">plugin</span> or <span class="at">instance</span> are required.


<span class="at">plugin</span>: <span class="at-val">string, optional</span>  
Plugin identifier, used for implicit plugin instantiation.



<span class="at">instance</span>: <span class="at-val">string, optional</span>  
Instance name, used for explicit plugin instantiation.


#### <span class="el-prefix">body/</span> ⁠ **site** ​

This element creates a site, which is a simplified and restricted kind of geom. A small subset of the geom attributes are available here; see the [geom](XMLreference.md) element for their detailed documentation. Semantically sites represent locations of interest relative to the body frames. Sites do not participate in collisions and computation of body masses and inertias. The geometric shapes that can be used to render sites are limited to a subset of the available geom types. However sites can be used in some places where geoms are not allowed: mounting sensors, specifying via-points of spatial tendons, constructing slider-crank transmissions for actuators.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the site.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">type</span>: <span class="at-val">\[sphere, capsule, ellipsoid, cylinder, box, mesh\], "sphere"</span>  
Type of geometric shape. This is used for rendering, and also determines the active sensor zone for [touch sensors](XMLreference.md).



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
Integer group to which the site belongs. This attribute can be used for custom tags. It is also used by the visualizer to enable and disable the rendering of entire groups of sites.



<span class="at">material</span>: <span class="at-val">string, optional</span>  
Material used to specify the visual properties of the site.



<span class="at">mesh</span>: <span class="at-val">string, optional</span>  
Mesh asset name. This attribute is required if the site type is "mesh".



<span class="at">rgba</span>: <span class="at-val">real(4), "0.5 0.5 0.5 1"</span>  
Color and transparency. If this value is different from the internal default, it overrides the corresponding material properties.



<span class="at">size</span>: <span class="at-val">real(3), "0.005 0.005 0.005"</span>  
Sizes of the geometric shape representing the site.



<span class="at">fromto</span>: <span class="at-val">real(6), optional</span>  
This attribute can only be used with capsule, cylinder, ellipsoid and box sites. It provides an alternative specification of the site length as well as the frame position and orientation. The six numbers are the 3D coordinates of one point followed by the 3D coordinates of another point. The elongated part of the site connects these two points, with the +Z axis of the site's frame oriented from the first towards the second point. The frame orientation is obtained with the same procedure as the zaxis attribute described in [Frame orientations](modeling.md). The frame position is in the middle between the two points. If this attribute is specified, the remaining position and orientation-related attributes are ignored.



<span class="at">pos</span>: <span class="at-val">real(3), "0 0 0"</span>  
Position of the site frame.







<span class="at">quat</span>, <span class="at">axisangle</span>, <span class="at">xyaxes</span>, <span class="at">zaxis</span>, <span class="at">euler</span>  
Orientation of the site frame. See [Frame orientations](modeling.md).







<span class="at">user</span>: <span class="at-val">real(nuser_site), "0 0 ..."</span>  
See [User parameters](modeling.md).


#### <span class="el-prefix">body/</span> ⁠ **camera** ​

This element creates a camera, which moves with the body where it is defined. To create a fixed camera, define it in the world body. The cameras created here are in addition to the default free camera which is always defined and is adjusted via the [visual](XMLreference.md) element. Internally MuJoCo uses a flexible camera model, where the viewpoint and projection surface are adjusted independently so as to obtain oblique projections needed for virtual environments. This functionality however is not accessible through MJCF. Instead, the cameras created with this element (as well as the free camera) have a viewpoint that is always centered in front of the projection surface. The viewpoint coincides with the center of the camera frame. The camera is looking along the -Z axis of its frame. The +X axis points to the right, and the +Y axis points up. Thus the frame position and orientation are the key adjustments that need to be made here.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the camera.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">mode</span>: <span class="at-val">\[fixed, track, trackcom, targetbody, targetbodycom\], "fixed"</span>  
This attribute specifies how the camera position and orientation in world coordinates are computed in forward kinematics (which in turn determine what the camera sees). "fixed" means that the position and orientation specified below are fixed relative to the body where the camera is defined. "track" means that the camera position is at a constant offset from the body in world coordinates, while the camera orientation is constant in world coordinates. These constants are determined by applying forward kinematics in qpos0 and treating the camera as fixed. Tracking can be used for example to position a camera above a body, point it down so it sees the body, and have it always remain above the body no matter how the body translates and rotates. "trackcom" is similar to "track" but the constant spatial offset is defined relative to the center of mass of the kinematic subtree starting at the body in which the camera is defined. This can be used to keep an entire mechanism in view. Note that the subtree center of mass for the world body is the center of mass of the entire model. So if a camera is defined in the world body in mode "trackcom", it will track the entire model. "targetbody" means that the camera position is fixed in the body frame, while the camera orientation is adjusted so that it always points towards the targeted body (which is specified with the target attribute below). This can be used for example to model an eye that fixates a moving object; the object will be the target, and the camera/eye will be defined in the body corresponding to the head. "targetbodycom" is the same as "targetbody" but the camera is oriented towards the center of mass of the subtree starting at the target body.



<span class="at">target</span>: <span class="at-val">string, optional</span>  
When the camera mode is "targetbody" or "targetbodycom", this attribute becomes required. It specifies which body should be targeted by the camera. In all other modes this attribute is ignored.



<span class="at">projection</span>: <span class="at-val">\[perspective, orthographic\], "perspective"</span>  
Whether the camera uses a perspective (the default) or orthographic projection. Setting this attribute to "orthographic" changes the semantic of the [fovy](XMLreference.md) attribute, see below.



<span class="at">fovy</span>: <span class="at-val">real, "45"</span>  
Vertical field-of-view of the camera. If the camera uses a perspective projection, the field-of-view is expressed in degrees, regardless of the global [compiler/angle](XMLreference.md) setting. If the camera uses an orthographic projection, the field-of-view is expressed in units of length; note that in this case the default of 45 is too large for most scenes and should likely be reduced. In either case, the horizontal field of view is computed automatically given the window size and the vertical field of view.



<span class="at">resolution</span>: <span class="at-val">int(2), "1 1"</span>  
Resolution of the camera in pixels \[width height\]. Note that these values are not used for rendering since those dimensions are determined by the size of the rendering context. This attribute serves as a convenient location to save the required resolution. Setting either value larger than 1 enables frustum visualization when the [mjVIS_CAMERA](APIreference/APItypes.md) visualization flag is active.



<span class="at">output</span>: <span class="at-val">\[rgb, depth, distance, normal, segmentation\], "rgb"</span>  
Types of output images supported by the camera.

- <span class="at-val">rgb</span>: RGB image.
- <span class="at-val">depth</span>: Depth image (distance from camera plane).
- <span class="at-val">distance</span>: Distance image (distance from camera origin).
- <span class="at-val">normal</span>: Surface normal image.
- <span class="at-val">segmentation</span>: Segmentation image.

This attribute is not used for rendering, but serves as a convenient location to save the output types supported by the camera. The <span class="at">output</span> attribute can contain multiple types, e.g. <span class="at-val">"rgb normal"</span>.



<span class="at">sensorsize</span>: <span class="at-val">real(2), "0 0"</span>  
Size of the camera sensor in length units. When specified, all intrinsic attributes become active and <span class="at">fovy</span> is ignored. The field-of-view is then computed automatically from the focal length and sensor size.




<span class="at">focal</span> / <span class="at">focalpixel</span>: <span class="at-val">real(2), "0 0"</span>  
Focal length in physical length units or in pixels, respectively. If both are specified, the pixel value is used and the length value is ignored.





<span class="at">principal</span> / <span class="at">principalpixel</span>: <span class="at-val">real(2), "0 0"</span>  
Offset of the principal point (optical axis intersection with the image plane) from the image center. If both are specified, the pixel value is used. At zero offset, the rendered image is centered on the camera's negative Z axis, as in a standard pinhole camera model.




<span class="at">ipd</span>: <span class="at-val">real, "0.068"</span>  
Inter-pupilary distance. This attribute only has an effect during stereoscopic rendering. It specifies the distance between the left and right viewpoints. Each viewpoint is shifted by +/- half of the distance specified here, along the X axis of the camera frame.



<span class="at">pos</span>: <span class="at-val">real(3), "0 0 0"</span>  
Position of the camera frame.







<span class="at">quat</span>, <span class="at">axisangle</span>, <span class="at">xyaxes</span>, <span class="at">zaxis</span>, <span class="at">euler</span>  
Orientation of the camera frame. See [Frame orientations](modeling.md). Note that specifically for cameras, the <span class="at">xyaxes</span> attribute is semantically convenient as the X and Y axes correspond to the directions "right" and "up" in pixel space, respectively.







<span class="at">user</span>: <span class="at-val">real(nuser_cam), "0 0 ..."</span>  
See [User parameters](modeling.md).


#### <span class="el-prefix">body/</span> ⁠ **light** ​

This element creates a light, which moves with the body where it is defined. To create a fixed light, define it in the world body. The lights created here are in addition to the optional [headlight](XMLreference.md), a camera-aligned light configured via the [visual](XMLreference.md) element. Lights shine along the direction specified by the dir attribute. They do not have a full spatial frame with three orthogonal axes.

By default, MuJoCo uses the standard OpenGL (fixed functional) Phong lighting model for its rendering, with augmented with shadow mapping. (See the OpenGL documentation for more information, including details about various attributes.)

MJCF also supports alternative lighting models (e.g. physically-based rendering) by providing additional attributes. Attributes may be applied or ignored depending on the lighting model being used.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the light.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">mode</span>: <span class="at-val">\[fixed, track, trackcom, targetbody, targetbodycom\], "fixed"</span>  
This is identical to the mode attribute of [camera](XMLreference.md) above. It specifies the how the light position and orientation in world coordinates are computed in forward kinematics (which in turn determine what the light illuminates).



<span class="at">target</span>: <span class="at-val">string, optional</span>  
This is identical to the target attribute of [camera](XMLreference.md) above. It specifies which body should be targeted in "targetbody" and "targetbodycom" modes.



<span class="at">type</span>: <span class="at-val">\[spot, directional, point, image\], "spot"</span>  
Determines the type of light. Note that some light types may not be supported by some renderers (e.g. only spot and directional lights are supported by the default native renderer).



<span class="at">directional</span>: <span class="at-val">\[false, true\], "false"</span>  
This is a deprecated legacy attribute. Please use light [type](XMLreference.md) instead. If set to "true", and no type is specified, this will change the light type to be directional.



<span class="at">castshadow</span>: <span class="at-val">\[false, true\], "true"</span>  
If this attribute is "true" the light will cast shadows. More precisely, geoms with [castshadow](XMLreference.md) enabled that are illuminated by the light will cast shadows. Since each shadow-casting light causes one extra rendering pass through all geoms, this attribute should be used with caution. Higher quality of the shadows is achieved by increasing the value of the shadowsize attribute of [quality](XMLreference.md), as well as positioning spotlights closer to the surface on which shadows appear, and limiting the volume in which shadows are cast. For spotlights this volume is a cone, whose angle is the cutoff attribute below multiplied by the shadowscale attribute of [map](XMLreference.md). For directional lights this volume is a box, whose half-sizes in the directions orthogonal to the light are the model extent multiplied by the shadowclip attribute of [map](XMLreference.md). The model extent is computed by the compiler but can also be overridden by specifying the extent attribute of [statistic](XMLreference.md). Internally the shadow-mapping mechanism renders the scene from the light viewpoint (as if it were a camera) into a depth texture, and then renders again from the camera viewpoint, using the depth texture to create shadows. The internal rendering pass uses the same near and far clipping planes as regular rendering, i.e., these clipping planes bound the cone or box shadow volume in the light direction. As a result, some shadows (especially those very close to the light) may be clipped.



<span class="at">active</span>: <span class="at-val">\[false, true\], "true"</span>  
The light is active if this attribute is "true". This can be used at runtime to turn lights on and off.



<span class="at">pos</span>: <span class="at-val">real(3), "0 0 0"</span>  
Position of the light. This attribute only affects the rendering for spotlights, but it should also be defined for directional lights because we render the cameras as decorative elements.



<span class="at">dir</span>: <span class="at-val">real(3), "0 0 -1"</span>  
Direction of the light.



<span class="at">diffuse</span>: <span class="at-val">real(3), "0.7 0.7 0.7"</span>  
The color of the light. For the Phong (default) lighting model, this defines the diffuse color of the light.



<span class="at">texture</span>: <span class="at-val">string, optional</span>  
The texture to use for image-based lighting. This is unused by the default Phong lighting model.



<span class="at">intensity</span>: <span class="at-val">real, "0.0"</span>  
The intensity of the light source, measured in candela, used for physically-based lighting models. This is unused by the default Phong lighting model.



<span class="at">ambient</span>: <span class="at-val">real(3), "0 0 0"</span>  
The ambient color of the light, used by the default Phong lighting model.



<span class="at">specular</span>: <span class="at-val">real(3), "0.3 0.3 0.3"</span>  
The specular color of the light, used by the default Phong lighting model.



<span class="at">range</span>: <span class="at-val">real, "10.0"</span>  
The effective range of the light. Objects further than this distance from the light position will not be illuminated by this light. This only applies to spotlights.



<span class="at">bulbradius</span>: <span class="at-val">real, "0.02"</span>  
The radius of the light-emitting surface. Larger radii produce softer shadows in renderers that support soft shadows. Ignored by the classic renderer.



<span class="at">attenuation</span>: <span class="at-val">real(3), "1 0 0"</span>  
These are the constant, linear and quadratic attenuation coefficients, used by the default Phong lighting model. The default corresponds to no attenuation. Physically-based lighting models instead attenuate with the inverse square of distance, scaled by [intensity](XMLreference.md) and limited by [range](XMLreference.md).



<span class="at">cutoff</span>: <span class="at-val">real, "45"</span>  
Cutoff angle for spotlights, always in degrees regardless of the global angle setting. The falloff of intensity inside the cone is controlled by [softness](XMLreference.md) for physically-based lighting models and by [exponent](XMLreference.md) for the default Phong lighting model.



<span class="at">softness</span>: <span class="at-val">real, "0.2"</span>  
Edge softness for spotlights, as a fraction of the [cutoff](XMLreference.md) angle in \[0, 1\], used by physically-based lighting models. The light delivers its full [intensity](XMLreference.md) inside the cone, falling to zero over the outer softness fraction of the cone angle; the default corresponds to a sharp-edged cone. This is unused by the default Phong lighting model, which uses [exponent](XMLreference.md).



<span class="at">exponent</span>: <span class="at-val">real, "10"</span>  
Exponent for spotlights, used by the default Phong lighting model. This setting controls the softness of the spotlight cutoff. Physically-based lighting models use [softness](XMLreference.md) instead.


#### <span class="el-prefix">body/</span> ⁠ **flexcomp** ​

This element is not a model element, but rather a macro which expands into multiple model elements representing a deformable entity. In particular this macro creates one [flex](XMLreference.md) element, a number of bodies that are children of the body in which the <span class="el">flexcomp</span> is defined, and optionally one [flex equality](XMLreference.md) which constrains all flex edges to their initial length. A number of attributes are specified here and then passed through to the automatically-constructed flex. The primary role of <span class="el">flexcomp</span> is to automate the creation of a (possibly large) collection of moving bodies with corresponding joints, and connect them with stretchable flex elements. See [flex](XMLreference.md) and [deformable objects](modeling.md) documentation for specifics on how flexes work. Here we only describe the automated construction process.

An important distinction between <span class="el">flex</span> and <span class="el">flexcomp</span> is that the flex references bodies and specifies vertex coordinates in the frames of those bodies, while the flexcomp defines *points*. Each flexcomp point corresponds to one body and one vertex in the underlying flex. If the flexcomp point is *pinned*, the corresponding flex body is the parent body of the flexcomp, while the corresponding flex vertex coordinates equal the flexcomp point coordinates. If the flexcomp point is not pinned, a new child body is created at the coordinates of the flexcomp point (within the flexcomp parent body), and then the coordinates of the flex vertex within that new body are (0,0,0). The mechanism for [pinning](XMLreference.md) flexcomp points is explained below.

Flexes generate their own collisions and shape-preserving forces, so the bodies created here need no geoms, sites or tendons. Most of the bodies created here have 3 orthogonal slider joints, corresponding to freely moving point masses. In some cases we generate radial slider joints, allowing only expansion and contraction, and for open-chain elastic 1D rods with $`n \ge 2`$ edges, extra per-edge `<name>_twist_0`, ..., `<name>_twist_{n-2}`, `<name>_twist` bodies and hinge joints are created under the world body to represent the edge twist angles (omitting `<name>_twist_0` when the first edge is clamped via `<pin id="0 1"/>`, and `<name>_twist` when the last two points of a rod with $`n \ge 3`$ edges are pinned). Since no geoms are generated, the bodies need to have explicit inertial parameters.

Below is a simple example of a flexcomp, modeling a (somewhat flexible) double pendulum with one end pinned to the world:

``` xml
<mujoco>
  <worldbody>
    <flexcomp name="FL" type="grid" dim="1" count="3 1 1" mass="3" spacing="0.2 0.2 0.2">
      <pin id="0"/>
    </flexcomp>
  </worldbody>
</mujoco>
```

This flexcomp has 3 points, however the first point is pinned to the world (i.e. the parent of the flexcomp) and so only two bodies are automatically created, namely FL_1 and FL_2. Here is what this flexcomp generates after loading and saving the XML:

``` xml
<mujoco>
  <worldbody>
    <body name="FL_1">
      <inertial pos="0 0 0" mass="1" diaginertia="1.66667e-05 1.66667e-05 1.66667e-05"/>
      <joint pos="0 0 0" axis="1 0 0" type="slide"/>
      <joint pos="0 0 0" axis="0 1 0" type="slide"/>
      <joint pos="0 0 0" axis="0 0 1" type="slide"/>
    </body>
    <body name="FL_2" pos="0.2 0 0">
      <inertial pos="0 0 0" mass="1" diaginertia="1.66667e-05 1.66667e-05 1.66667e-05"/>
      <joint pos="0 0 0" axis="1 0 0" type="slide"/>
      <joint pos="0 0 0" axis="0 1 0" type="slide"/>
      <joint pos="0 0 0" axis="0 0 1" type="slide"/>
    </body>
  </worldbody>
  <deformable>
    <flex name="FL" dim="1" body="world FL_1 FL_2" vertex="-0.2 0 0 0 0 0 0 0 0" element="0 1 1 2"/>
  </deformable>
  <equality>
    <flex flex="FL"/>
  </equality>
</mujoco>
```


<span class="at">name</span>: <span class="at-val">string, required</span>  
The name of the flex element being generated automatically. This name is used as a prefix for all bodies that are automatically generated here, and is also referenced by the corresponding flex equality constraint (if applicable).



<span class="at">dim</span>: <span class="at-val">int(1), "2"</span>  
Dimensionality of the flex object. This value must be 1, 2 or 3. The flex elements are capsules in 1D, triangles with radius in 2D, and tetrahedra with radius in 3D. Certain flexcomp types imply a dimensionality, in which case the value specified here is ignored.



uNt3i8hrJu4



<span class="at">dof</span>: <span class="at-val">\[full, radial, trilinear, quadratic, 2d\], "full"</span>  
The parametrization of the flex's degrees of freedom (dofs). See the video on the right illustrating the different parametrizations with deformable spheres. The three models in the video are respectively [sphere_full](https://github.com/google-deepmind/mujoco/blob/main/model/flex/sphere_full.xml), [sphere_radial](https://github.com/google-deepmind/mujoco/blob/main/model/flex/sphere_radial.xml) and [sphere_trilinear](https://github.com/google-deepmind/mujoco/blob/main/model/flex/sphere_trilinear.xml).

**full**  
Three translational dofs per vertex. This is the most expressive but also the most expensive option.

**radial**  
A single radial translational dof per vertex. Note that unlike in the "full" case, the radial parametrization requires a free joint at the flex's parent in order for free body motion to be possible. This type of parametrization is appropriate for shapes that are relatively spherical.

**2d**  
Two orthogonal translational dofs (X and Y) per vertex. This restricts the motion of the vertices to planes parallel to the parent body's X-Y plane.

**trilinear**  
Three translational dofs at each corner of the bounding box of the flex, for a total of 24 dofs for the entire flex, independent of the number of vertices. The positions of the vertices are updated using trilinear interpolation over the bounding box.


qJFbx-FR7Bc


Trilinear and quadratic flexes are much faster than the previous two options, and are the preferred choice if the expected deformations can be captured by the reduced parametriation. For example, see the video on the right comparing [full](https://github.com/google-deepmind/mujoco/blob/main/model/flex/gripper.xml) and [trilinear](https://github.com/google-deepmind/mujoco/blob/main/model/flex/gripper_trilinear.xml) flexes for modeling deformable gripper pads.

Note that the choice of dof parametrization affects the deformation modes of the flex but has no effect on the accuracy of the collision geometry, which always takes into account the high-resolution mesh of the flex.

**quadratic**  
Three translational dofs per corner, edge, face, and volume of the bounding box of the flex, for a total of 81 dofs for the entire flex, independent of the number of vertices. The positions of the vertices are updated using quadratic interpolation over the bounding box. While this option requires more degrees of freedom than trilinear flexes, it enables curved deformation modes, while the only modes achievable for trilinear flexes are stretch/compression and shear. To understand the difference between the two parametrizations, see [a trilinear cube](https://github.com/google-deepmind/mujoco/blob/main/model/flex/trilinear.xml) and [a quadratic cube](https://github.com/google-deepmind/mujoco/blob/main/model/flex/quadratic.xml).

Note that a higher interpolation order generally requires a smaller time step for stability, although usually not as large as with the "full" option and a fine mesh.

For **full**, **trilinear**, and **quadratic** parametrizations (with `rigid="false"`), the generated vertex or node child bodies already carry 3 orthogonal translational slide joints. Unless at least one active vertex or node is [pinned](XMLreference.md) to the parent body, the parent body (and its ancestor bodies) must not have a `<freejoint/>` or other joints.



<span class="at">type</span>: <span class="at-val">\[grid, box, cylinder, ellipsoid, disc, circle, mesh, gmsh, direct\], "grid"</span>  
This attribute determines the type of <span class="el">flexcomp</span> object. The remaining attributes and sub-elements are then interpreted according to the type. Default settings are also adjusted depending on the type. Different types correspond to different methods for specifying the flexcomp points and the stretchable elements that connect them. They fall in three categories: direct specification entered in the XML, direct specification loaded from file, and automated generation from higher-level specification.

**grid** generates a rectangular grid of points in 1D, 2D or 3D as specified by <span class="at">dim</span>. The number of points in each dimension is determined by <span class="at">count</span> while the grid spacing in each dimension is determined by <span class="at">spacing</span>. Make sure the spacing is sufficiently large relative to <span class="at">radius</span> to avoid permanent contacts. In 2D and 3D the grid is automatically triangulated, and corresponding flex elements are created (triangles or tetrahedra). In 1D the elements are capsules connecting consecutive pairs of points.

**box** generates a 3D box object, however flex bodies are only generated on the outer shell. Each flex body has a radial slider joint allowing it to move in and out from the center of the box. The parent body would normally be a floating body. The box surface is triangulated, and when <span class="at">dim=3</span> (default) each flex element is a tetrahedron connecting the center of the box with one triangle face. When <span class="at">dim=2</span>, an open-top surface shell of triangle elements is generated (the `+z` top face is omitted, as in `model/flex/basket.xml`). <span class="at">count</span> and <span class="at">spacing</span> determine the count and spacing of the flex bodies, similar to the **grid** type in 3D.

**cylinder** is the same as **box**, except the points are projected on the surface of a cylinder (when <span class="at">dim=2</span>, the `+z` top face is likewise omitted).

**ellipsoid** is the same as **box**, except the points are projected on the surface of an ellipsoid (when <span class="at">dim=2</span>, the `+z` top cap is likewise omitted).

**disc** is the same as **box**, except the points are projected on the surface of a disc. It is only compatible with <span class="at">dim=2</span>.

**circle** is the same as **grid**, except the points are sampled along a circle so that the first and last points are the same. The radius of the circle is computed such that each segment has the requested spacing. It is only compatible with <span class="at">dim=1</span>.

**mesh** loads the flexcomp points and elements (i.e. triangles) from a mesh file, in the same file formats as mesh assets, excluding the legacy .msh format. A mesh asset is not actually added to the model. Instead the vertex and face data from the mesh file are used to populate the point and element data of the flexcomp. <span class="at">dim</span> is automatically set to 2. Recall that a mesh asset in MuJoCo can be used as a rigid geom attached to a single body. In contrast, the flex generated here corresponds to a soft mesh with the same initial shape, where each vertex is a separate moving body (unless pinned).


**gmsh** is similar to mesh, but it loads a GMSH file in [format 4.1](https://gmsh.info//doc/texinfo/gmsh.html#MSH-file-format) and [format 2.2](https://gmsh.info//doc/texinfo/gmsh.html#MSH-file-format-version-2-_0028Legacy_0029) (ascii or binary). The file extension can be anything; the parser recognizes the format by examining the file header. This is a very rich file format, allowing all kinds of elements with different dimensionality and topology. MuJoCo only supports GMSH element types 2 and 4 which happen to correspond to our 2D and 3D flexes and assumes that the nodes are specified in a single block. Only the Nodes and Elements sections of the GMHS file are processed, and used to populate the point and element data of the flexcomp. The parser will generate an error if the GMSH file contains meshes that are not supported by MuJoCo. <span class="at">dim</span> is automatically set to the dimensionality specified in the GMSH file. Presently this is the only mechanism to load a large tetrahedral mesh in MuJoCo and generate a corresponding soft entity. If such a mesh is available in a different file format, use the freely available [GMSH software](https://gmsh.info/) to convert it to GMSH in one of the supported versions.


**direct** allows the user to specify the point and element data of the flexcomp directly in the XML. Note that flexcomp will still generate moving bodies automatically, as well as automate other settings; so it still provides convenience compared to specifying the corresponding flex directly.



<span class="at">count</span>: <span class="at-val">int(3), "10 10 10"</span>  
Specifies the number of automatically generated points in each dimension for types **grid**, **box**, **cylinder**, and **ellipsoid**.



<span class="at">cellcount</span>: <span class="at-val">int(3), "1 1 1"</span>  
Specifies the number of cells in each dimension for the background interpolation grid when using **trilinear** or **quadratic** dofs. Compilation and simulation cost scale with `cellcount` and the interpolation order ([dof](XMLreference.md)); compiled cell stiffness and cut-cell quadrature weights are cached across recompilations.



<span class="at">spacing</span>: <span class="at-val">real(3), "0.02 0.02 0.02"</span>  
The spacing between the automatically generated points in each dimension. The spacing should be sufficiently large compared to the radius, to avoid permanent contacts.



<span class="at">point</span>: <span class="at-val">real(3\*npoint), optional</span>  
The 3D coordinates of the points. This attribute is only used with type **direct**. All other flexcomp types generate their own points. The points are used to construct bodies and vertices as explained earlier.



<span class="at">element</span>: <span class="at-val">int((dim+1)\*npoint), optional</span>  
The zero-based point ids forming each flex elements. This attribute is only used with type **direct**. All other flexcomp types generate their own elements. This data is passed through to the automatically-generated flex.



<span class="at">texcoord</span>: <span class="at-val">real(2\*npoint), optional</span>  
Texture coordinates of each point, passed through to the automatically-generated flex. Note that flexcomp does not generate texture coordinates automatically, except for 2D grids, box, cylinder and ellipsoid. For all other types, the user can specify explicit texture coordinates here, even if the points themselves were generated automatically. This requires understanding of the layout of the automatically-generated points and how they correspond to the texture referenced by the material.



<span class="at">mass</span>: <span class="at-val">real(1), "1"</span>  
The mass of each automatically-generated body equals this value divided by the number of points. Note that pinning some points does not affect the mass of the other bodies.



<span class="at">inertiabox</span>: <span class="at-val">real(1), "0.005"</span>  
Even though the automatically-generated bodies have the physics of point masses, with slider joints, MuJoCo still requires each body to have rotational inertia. The inertias generated here are diagonal, and are computed such that the corresponding equivalent-inertia boxes have sides equal to this value.



<span class="at">file</span>: <span class="at-val">string, optional</span>  
The name of the file from which a **surface** (triangular) or **volumetric** (tetrahedral) mesh is loaded. For surface meshes, the file extension is used to determine the file format. Supported formats are GMSH and the formats specified in [mesh assets](XMLreference.md), excluding the legacy .msh format. Volumetric meshes are supported only in GMSH format. See *here* for more information on GMSH files.



<span class="at">mesh</span>: <span class="at-val">string, optional</span>  
The name of a [mesh asset](XMLreference.md) from which a **surface** (triangular) or **volumetric** (tetrahedral) mesh is referenced. Can be used in place of <span class="at">file</span>. If specified without an explicit <span class="at">type</span>, the flexcomp type defaults to `mesh`; any type other than `mesh` or `gmsh` is an error. The asset's <span class="at">scale</span>, <span class="at">refpos</span> and <span class="at">refquat</span> are applied to the vertices and volumetric nodes, which are otherwise expressed in the frame of the asset, so that the flex coincides with a geom using the same mesh at the same position. In contrast, <span class="at">file</span> uses the raw file coordinates. For <span class="at">dim</span> = 3, <span class="at">origin</span> is expressed in the same frame. The mesh asset is read when the flexcomp is expanded, i.e. when the model is parsed or *mjs_makeFlex* is called, so later changes to the mesh asset do not affect the flex.



<span class="at">rigid</span>: <span class="at-val">\[true, false\], "false"</span>  
If this is true, all points correspond to vertices within the parent body, and no new bodies are created. This is equivalent to pinning all points. Note that if all points are indeed pinned, the model compiler will detect that the flex is rigid (which behaves is a non-convex mesh in collision detection).



<span class="at">pos</span>: <span class="at-val">real(3), "0 0 0"</span>  
This 3D vector translates all points relative to the frame of the parent body.



<span class="at">quat</span>: <span class="at-val">real(4), "1 0 0 0"</span>  
This is a quaternion rotation of all points around the <span class="at">pos</span> vector specified above. Together these two vectors define a pose transformation, used to position and orient the points as needed.






<span class="at">axisangle</span>, <span class="at">xyaxes</span>, <span class="at">zaxis</span>, <span class="at">euler</span>  
Alternative specification of rotation, that can be used instead of <span class="at">quat</span>.






<span class="at">scale</span>: <span class="at-val">real(3), "1 1 1"</span>  
Scaling of all point coordinates, for types that specify coordinates explicitly. Scaling is applied before the pose transformation.







<span class="at">radius</span>, <span class="at">material</span>, <span class="at">rgba</span>, <span class="at">group</span>, <span class="at">flatskin</span>  
These attributes are directly passed through to the automatically-generated [flex](XMLreference.md) object and have the same meaning.







<span class="at">origin</span>: <span class="at-val">real(3), "0 0 0"</span>  
The origin of the flexcomp. Used for generating a volumetric mesh from an OBJ surface mesh. Each surface triangle is connected to the origin to create a tetrahedron, so the resulting volumetric mesh is guaranteed to be well-formed only for convex shapes.


##### <span class="el-prefix">flexcomp/</span> ⁠ **contact** ​





























<span class="at">internal</span>, <span class="at">selfcollide</span>, <span class="at">activelayers</span>, <span class="at">contype</span>, <span class="at">conaffinity</span>, <span class="at">condim</span>, <span class="at">priority</span>, <span class="at">friction</span>, <span class="at">solmix</span>, <span class="at">solimp</span>, <span class="at">margin</span>, <span class="at">gap</span>  
Same as in [flex/contact](XMLreference.md). All attributes are passed through to the automatically-generated flex.

##### <span class="el-prefix">flexcomp/</span> ⁠ **edge** ​

Each flex element has one edge in 1D (coinciding with the capsule element), three edges in 2D, and six edges in 3D. The edges are generated automatically when the flex element is compiled, and the user cannot specify them directly. This element is used to adjust the properties of all edges in the flex.


<span class="at">equality</span>: <span class="at-val">\[false, true, strain\], "false"</span>  
The type of equality constraint applied to this edge. If <span class="at-val">false</span>, no equality constraint is applied. If <span class="at-val">true</span>, then edge constraints are enforced. If <span class="at-val">strain</span>, then a constraint is added to enforce that the invariants of the strain tensor do not change; this is the only equality constraint type supported for trilinear and quadratic [dofs](XMLreference.md) elements, see [here](XMLreference.md).




<span class="at">solref</span>, <span class="at">solimp</span>  
The standard constraint parameters, passed through to the automatically generated equality constraint.





<span class="at">stiffness</span>, <span class="at">damping</span>  
Edge stiffness and damping, passed through to the automatically generated flex.



##### <span class="el-prefix">flexcomp/</span> ⁠ **elasticity** ​



















<span class="at">young</span>, <span class="at">poisson</span>, <span class="at">shear</span>, <span class="at">damping</span>, <span class="at">thickness</span>, <span class="at">yield</span>, <span class="at">elastic2d</span>, <span class="at">section</span>, <span class="at">sectionsize</span>  
Same as in [flex/elasticity](XMLreference.md). All attributes are passed through to the automatically-generated flex. In particular, <span class="at">yield</span> takes one or two values, for stretching and bending; a single value is also the bending yield strain only if the generated flex is a non-interpolated 2D flex.

##### <span class="el-prefix">flexcomp/</span> ⁠ **pin** ​

Each point is either pinned or not pinned. The effect of pinning was explained earlier. This element is used to specify which points are pinned. Note that each attribute below can be used to specify multiple pins, and in addition to that, the <span class="el">pin</span> element itself can be repeated for user convenience. The effects are cumulative; pinning the same point multiple times is allowed.

For interpolated flexcomps (**trilinear** or **quadratic** [dof](XMLreference.md)), degrees of freedom live on a 3D grid of `order * cellcount + 1` nodes per axis (`order` = 1 for **trilinear**, 2 for **quadratic**; see [cellcount](XMLreference.md)) rather than at mesh vertices. Pinning fixes these nodes: <span class="at">id</span> and <span class="at">range</span> use linear node indices (`z` fastest, then `y`, `x`), while <span class="at">grid</span> and <span class="at">gridrange</span> use node coordinates regardless of flexcomp [type](XMLreference.md) (for <span class="at">dim</span> 2 or 3).


<span class="at">id</span>: <span class="at-val">int(n), required</span>  
Zero-based ids of points to pin. When the points are automatically-generated, the user needs to understand their layout in order to decide which points to pin. This can be done by first creating a flexcomp without any pins, loading it in the simulator, and showing the body labels. For open-chain 1D elastic rods, `<pin id="0 1"/>` clamps the first edge and its material frame to the parent body (omitting `<name>_twist_0`), whereas `<pin id="0"/>` anchors only the first point (a spherical joint) while keeping `<name>_twist_0` free.



<span class="at">range</span>: <span class="at-val">int(2\*n), required</span>  
Ranges of points to pin. Each range is specified by two integers.



<span class="at">grid</span>: <span class="at-val">int(dim\*n), required</span>  
Grid coordinates of points or interpolation nodes to pin. This can only be used with <span class="at">dim</span> 2 or 3, and requires type **grid** or an interpolated [dof](XMLreference.md) (**trilinear** or **quadratic**).



<span class="at">gridrange</span>: <span class="at-val">int(2\*dim\*n), required</span>  
Ranges of grid coordinates of points or interpolation nodes to pin. Each range is specified by (dim) integers for the minimum of the range followed by (dim) integers for the maximum of the range. This can only be used with <span class="at">dim</span> 2 or 3, and requires type **grid** or an interpolated [dof](XMLreference.md) (**trilinear** or **quadratic**).


##### <span class="el-prefix">flexcomp/</span> ⁠ **plugin** `dot`

Associate this flexcomp with an [engine plugin](programming/extension.md). Either <span class="at">plugin</span> or <span class="at">instance</span> are required.


<span class="at">plugin</span>: <span class="at-val">string, optional</span>  
Plugin identifier, used for implicit plugin instantiation.



<span class="at">instance</span>: <span class="at-val">string, optional</span>  
Instance name, used for explicit plugin instantiation.


#### <span class="el-prefix">body/</span> ⁠ **plugin** `dot`

Associate this body with an [engine plugin](programming/extension.md). Either <span class="at">plugin</span> or <span class="at">instance</span> are required.


<span class="at">plugin</span>: <span class="at-val">string, optional</span>  
Plugin identifier, used for implicit plugin instantiation.



<span class="at">instance</span>: <span class="at-val">string, optional</span>  
Instance name, used for explicit plugin instantiation.


#### <span class="el-prefix">body/</span> ⁠ **attach** ​

The <span class="el">attach</span> element is used to insert elements from another (child) model, or from the current model itself (self-attachment), into this (parent) model's kinematic tree. Unlike [include](XMLreference.md), which is implemented in the parser and is equivalent to copying and pasting XML from one file into another, <span class="el">attach</span> is implemented in the model compiler. In order to use this element to import from another model, the sub-model must first be defined as an [asset](XMLreference.md). When creating an attachment, a frame, body or the entire child model in the child model is specified, and all referencing elements outside the kinematic tree (e.g., sensors and actuators), are also copied into the parent model. Additionally, any elements referenced from within the attached subtree (e.g. defaults and assets) will be copied in to the parent model. For self-attaching within the same model, the <span class="at">model</span> attribute is omitted, and a body or frame must be specified. <span class="el">attach</span> is a [Meta elements](XMLreference.md), so upon saving all attachments will appear in the saved XML file. Note that this element is a subset of the functionality of the procedural [attachment](programming/modeledit.md) functionality. As such, it shares the same limitations as described there. See example [here](https://github.com/google-deepmind/mujoco/blob/main/test/xml/testdata/parent.xml).


Known issues

The following known limitations exist, to be addressed in a future release:

- All assets from the child model will be copied in, whether they are referenced or not.
- Circular references are not checked for and will lead to infinite loops.



<span class="at">model</span>: <span class="at-val">string, optional</span>  
The child model from which to attach a subtree or a frame. If omitted, the attachment is performed within the current model (self-attachment).



<span class="at">body</span>: <span class="at-val">string, optional</span>  
Name of the body in the child model to attach here. The body and its subtree will be attached. If neither this attribute nor [frame](XMLreference.md) is specified (only one allowed), the contents of the world body will be attached in a new [frame](XMLreference.md).



<span class="at">frame</span>: <span class="at-val">string, optional</span>  
Name of the frame in the child model to attach here. If neither this attribute nor [body](XMLreference.md) is specified (only one allowed), the contents of the world body will be attached in a new [frame](XMLreference.md). Frames which enclose it in the child model are not attached.



<span class="at">prefix</span>: <span class="at-val">string, required</span>  
Prefix to prepend to names of elements in the child model. This attribute is required to prevent name collisions with the parent or when attaching the same sub-tree multiple times.


#### <span class="el-prefix">body/</span> ⁠ **frame** ​

Frames specify a coordinate transformation which is applied to all child elements. During compilation the transformation they encode is accumulated in their direct children; frames are preserved when the model is saved.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the frame.



<span class="at">childclass</span>: <span class="at-val">string, optional</span>  
If this attribute is present, all descendant elements that admit a defaults class will use the class specified here, unless they specify their own class or another frame or body with a childclass attribute is encountered along the chain of nested bodies and frames. Recall [Default settings](modeling.md).



<span class="at">pos</span>: <span class="at-val">real(3), "0 0 0"</span>  
The 3D position of the frame, in the parent coordinate system.







<span class="at">quat</span>, <span class="at">axisangle</span>, <span class="at">xyaxes</span>, <span class="at">zaxis</span>, <span class="at">euler</span>  
See [Frame orientations](modeling.md).







<span class="at">scale</span>: <span class="at-val">real(1 or 3), "1"</span>  
Resizes everything inside the frame. Bodies, geoms, sites, joints and all other contents are scaled about the frame's origin, while the frame's own <span class="at">pos</span> and orientation, which are in its parent's coordinates, are not. Scaling happens at compile time: the spec keeps the authored values, so changing the scale and recompiling starts again from them, and a model saved as written keeps the attribute.

Three attributes work together. <span class="at">scale</span> sets the factor $`s`$ of lengths, [massscale](XMLreference.md) the factor $`m`$ of masses, by default $`s^3`$ (the same material), and [scaling](XMLreference.md) decides whether forces, stiffnesses and actuator gains follow (`similar`, the default) or keep their authored values (`geometry`). Typical uses:

| intent | attributes |
|----|----|
| a copy which moves like the original, in proportionally scaled gravity | `scale="s"` |
| a larger or smaller body of the same material, with the same motors and springs | `scale="s" scaling="geometry"` |
| a larger or smaller body of the same mass | `scale="s" scaling="geometry" massscale="1"` |
| a heavier or lighter body of the same size, e.g. a payload | `massscale="k" scaling="geometry"` |
| a change of the units of length and mass | `scale="s" massscale="k"` |
| a body stretched along the frame's axes, see below | `scale="sx sy sz" scaling="geometry"` |

Scales of nested frames compose by multiplication. A single value applies to all three axes. Values must be finite and positive.

Three different values stretch the contents along the frame's axes, which requires <span class="at">scaling</span> "geometry". Positions are mapped exactly and orientations are kept, so each shape inside is stretched in its own coordinates, which only some shapes can represent:

- meshes always, with an instance of the mesh for each distinct stretch;
- boxes, ellipsoids, planes and height fields aligned with the frame's axes;
- capsules and cylinders aligned with the frame's axes and stretched equally across their own axis. The caps of a capsule stay hemispherical: with $`a`$ the factor across its axis and $`c`$ the factor along it, its radius $`r`$ becomes $`a r`$ and its half-length $`h`$ becomes $`c h`$, so that its total length is $`2 (c h + a r)`$ rather than $`2 c (h + r)`$;
- spheres only when scaled uniformly; use an ellipsoid otherwise.

Hinge and slide joints must also be aligned with the frame's axes. Anything else is a compile error; alignment is checked to within about 2 degrees. Sites are never an error: a site box, ellipsoid, capsule or cylinder is stretched by the factor along each of its own axes, with the radius of a capsule or cylinder taking the geometric mean of the two factors across it, which is approximate when the site is not aligned. Explicit inertias transform exactly. Sphere sites, and lengths without a direction like margins, contact widths and tendon widths, take the geometric mean of the three factors.

A mesh or height field used at several scales compiles to an instance per scale; the first keeps its name and the others are named `name@1`, `name@2`, ... A model saved compiled writes a mesh instance which is not stretched along its own axes as vertices and faces; its texture coordinates are kept only if they are given per vertex, and its normals are recomputed. The bones of a skin must have the same scale, and elements with plugins and tactile sensors cannot be scaled.



<span class="at">scaling</span>: <span class="at-val">\[similar, geometry\], "similar"</span>  
What changes along with size and mass. With $`s`$ the <span class="at">scale</span> and $`m`$ the <span class="at">massscale</span>:

similar  
A change of the units of length and mass: every quantity of dimension $`L^a M^b T^c`$ is multiplied by $`s^a m^b`$. Positions and sizes are multiplied by $`s`$, masses by $`m`$, rotational inertias and torques by $`m s^2`$, forces by $`m s`$, the stiffness of a slide joint by $`m`$; times and angles are unchanged. The scaled model moves exactly like the original would in gravity $`g/s`$. Gravity itself is not scaled, so relative to the model's own forces it is weaker by $`1/s`$.

geometry  
Only geometry and inertia change: lengths are multiplied by $`s`$, masses by $`m`$ and rotational inertias by $`m s^2`$, while stiffness, damping, armature, friction loss, force limits and actuator gains keep their authored values. Quantities specified in the time domain, like [springdamper](XMLreference.md) or a servo's <span class="at">dampratio</span>, keep that specification, so the stiffness and damping computed from them follow the inertia.

The policy applies to this frame's <span class="at">scale</span> and <span class="at">massscale</span> only, and is not inherited by nested frames.



<span class="at">massscale</span>: <span class="at-val">real, "0"</span>  
Factor $`m`$ of the masses of the frame's contents: masses are multiplied by $`m`$, rotational inertias by $`m s^2`$ and densities by $`m / s^3`$. The default 0 means $`m = s_x s_y s_z`$, the ratio of volumes, which keeps densities constant. Under `similar` scaling $`m`$ is also the factor of the unit of mass, which forces follow. Values must be finite and non-negative. Factors of nested frames compose by multiplication, so <span class="at">massscale</span> "1" in an inner frame is relative to the enclosing frames.


### **contact** ​

This is a grouping element and does not have any attributes. It groups elements that are used to adjust the generation of candidate contact pairs for collision checking. [Collision detection](computation/index.md) was described in detail in the Computation chapter, thus the description here is brief.

#### <span class="el-prefix">contact/</span> ⁠ **pair** ​

This element creates a predefined geom pair which will be checked for collision. Unlike dynamically generated pairs whose properties are inferred from the corresponding geom properties, the pairs created here specify all their properties explicitly or through defaults, and the properties of the individual geoms are not used. Anisotropic friction can only be created with this element.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of this contact pair.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">geom1</span>: <span class="at-val">string, required</span>  
The name of the first geom in the pair.



<span class="at">geom2</span>: <span class="at-val">string, required</span>  
The name of the second geom in the pair. The contact force vector computed by the solver and stored in mjData.efc_force points from the first towards the second geom by convention. The forces applied to the system are of course equal and opposite, so the order of geoms does not affect the physics.



<span class="at">condim</span>: <span class="at-val">int, "3"</span>  
The dimensionality of the contacts generated by this geom pair.



<span class="at">friction</span>: <span class="at-val">real(5), "1 1 0.005 0.0001 0.0001"</span>  
The friction coefficients of the contacts generated by this geom pair. Making the first two coefficients different results in anisotropic tangential friction. Making the last two coefficients different results in anisotropic rolling friction. The length of this array is not enforced by the parser, and can be smaller than 5. This is because some of the coefficients may not be used, depending on the contact dimensionality. Unspecified coefficients remain equal to their defaults.




<span class="at">solref</span>, <span class="at">solimp</span>  
Constraint solver parameters for contact simulation. See [Solver parameters](modeling.md).




<span class="at">solreffriction</span>: <span class="at-val">real, "0 0"</span>  
Contact reference acceleration, in the friction dimensions. This attribute has the same semantics as other <span class="at">solref</span> attributes (described in [Solver parameters](modeling.md)), with two important distictions:

- The default <span class="at-val">"0 0"</span> means "use the same values as <span class="at">solref</span>".
- This attribute only takes effect for [elliptic friction cones](XMLreference.md), since pyramidal cones mix normal and frictional forces.

Note that as with other <span class="at">solreffriction</span> attributes, the constraint violation is identically 0. Therefore, when using positive semantics <span class="at">solreffriction\[1\]</span> is ignored, while for negative semantics <span class="at">solreffriction\[0\]</span> is ignored. See [Friction](modeling.md) for more details.



<span class="at">margin</span>: <span class="at-val">real, "0"</span>  
Geometric inflation for the purpose of contact force generation. Contacts are detected at distance `margin + gap` and forces are generated at distance `margin`.



<span class="at">gap</span>: <span class="at-val">real, "0"</span>  
Additional contact detection buffer beyond `margin`. When this value is positive, contacts with distance between `margin` and `margin + gap` are included in `mjData.contact` as inactive contacts but no contact forces are generated.



<span class="at">adhesion</span>: <span class="at-val">real, "0"</span>  
Adhesive force of contacts generated by this pair, overriding the sum of the geoms' [adhesion](XMLreference.md) values. See there for detailed semantics.


#### <span class="el-prefix">contact/</span> ⁠ **exclude** ​

This element is used to exclude a pair of bodies from collision checking. Unlike all other contact-related elements which refer to geoms, this element refers to bodies. Experience has shown that exclusion is more useful on the level of bodies. Collisions between any geom defined in the first body and any geom defined in the second body are excluded.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of this exclude pair.



<span class="at">body1</span>: <span class="at-val">string, required</span>  
The name of the first body in the pair.



<span class="at">body2</span>: <span class="at-val">string, required</span>  
The name of the second body in the pair.


### **deformable** ​

This is a grouping element and does not have any attributes. It groups elements that specify deformable objects, namely flexes and skins.

#### <span class="el-prefix">deformable/</span> ⁠ **flex** ​

Flexible objects (or flexes) are collections of massless stretchable geometric elements (capsules, triangles or tetrahedra) connecting vertices that are defined within different moving body frames. These stretchable elements support collisions and contact forces, which are then distributed to all the interconnected bodies. Flexes also generate passive and constraint forces as needed to simulate deformable entities with the desired material properties. The modeling of flexes is automated and simplified by the [flexcomp](XMLreference.md) element. In most cases, the user will specify a <span class="el">flexcomp</span> which will then automatically construct the corresponding low-level <span class="el">flex</span>. See [deformable objects](modeling.md) for additional information.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the flex.



<span class="at">dim</span>: <span class="at-val">int, "2"</span>  
Dimensionality of the flex. Allowed values are 1, 2 and 3. In 1D the elements are capsules, in 2D the elements are triangles with radius, in 3D the elements are tetrahedra with (optional) radius.



<span class="at">radius</span>: <span class="at-val">real, "0.005"</span>  
Radius of all flex elements. It can be zero in 3D, but must be positive in 1D and 2D. The radius affects both collision detection and rendering. In 1D and 2D it is needed to make the elements volumetric.



<span class="at">body</span>: <span class="at-val">string(nvert or 1), required</span>  
An array of MuJoCo body names (separated by white space) to which each vertex belongs. The number of body names should either equal the number of vertices (nvert), or be a single body. If a single body is specified, all vertices are defined within that body - in which case the flex becomes a rigid body. The latter functionality effectively creates a general non-convex mesh (unlike mesh geoms which are convexified for collision detection purposes).



<span class="at">vertex</span>: <span class="at-val">real(3\*nvert), optional</span>  
The local coordinates of the vertices within the corresponding body frames. If this attribute is omitted, all coordinates are (0,0,0) or in other words, the vertices coincide with the centers of the body frames.



<span class="at">texcoord</span>: <span class="at-val">real(2\*vert or ntexcoord), optional</span>  
Texture coordinates. If omitted, texture mapping for this flex is disabled, even if a texture is specified in the material.



<span class="at">elemtexcoord</span>: <span class="at-val">int((dim+1)\*nelem), optional</span>  
Texture indices for each face. If omitted, texture are assumed to be vertex-based.



<span class="at">element</span>: <span class="at-val">int((dim+1)\*nelem), required</span>  
For each element of the flex, this lists the zero-based indices of the vertices forming that flex element. We need two vertices to specify a capsule, three vertices to specify a triangle, and four vertices to specify a tetrahedron - which is why the number of indices equals (dim+1) times the number of elements. In 2D, the vertices should be listed in counter-clockwise order. In 1D and 3D the order is irrelevant; in 3D the model compiler will rearrange the vertices as needed. Repeated vertex indices within a flex element are not allowed. The topology of the flex is not enforced; it could correspond to a continuous soft body, or a collection of disconnected stretchable elements, or anything in-between.



<span class="at">flatskin</span>: <span class="at-val">\[true, false\], "false"</span>  
This attribute determines whether 2D and 3D flexes that are rendered in flexskin mode will use smooth or flat shading. The default smooth shading is suitable in most cases, however if the object is intended to have visible sharp edges (such as a cube) then flat shading is more natural.



<span class="at">material</span>: <span class="at-val">string, optional</span>  
If specified, this attribute applies a [material](XMLreference.md) to the flex. Note that textures specified in the material will be applied only if the flex has explicit texture coordinates.



<span class="at">rgba</span>: <span class="at-val">real(4), "0.5 0.5 0.5 1"</span>  
Instead of creating material assets and referencing them, this attribute can be used to set color and transparency only. This is not as flexible as the material mechanism, but is more convenient and is often sufficient. If the value of this attribute is different from the internal default, it takes precedence over the material.



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
Integer group to which the flex belongs. This attribute can be used for custom tags. It is also used by the visualizer to enable and disable the rendering of entire groups of flexes.



<span class="at">node</span>: <span class="at-val">string(nnode), optional</span>  
The degrees-of-freedom of the flex. An array of MuJoCo body names (separated by white space) to which each node belongs. The number of body names should equal the number of nodes (nnode). See the flexcomp [dof](XMLreference.md) attribute for more details.



<span class="at">nodecoord</span>: <span class="at-val">real(3\*nnode), optional</span>  
The local coordinates of the nodes within the corresponding body frames. If this attribute is omitted, all coordinates are (0,0,0) or in other words, the nodes coincide with the centers of the body frames. Nonzero coordinates are required when several nodes share a body, for example nodes pinned to a parent body.



<span class="at">cellcount</span>: <span class="at-val">int(3), optional</span>  
When using **trilinear** or **quadratic** dofs, this specifies the number of cells in each dimension for the background interpolation grid.



<span class="at">dof</span>: <span class="at-val">\[trilinear, quadratic\], optional</span>  
Interpolation order for the flex.


##### <span class="el-prefix">flex/</span> ⁠ **edge** `dot`

This element adjusts the passive or constraint properties of all edges of the flex. A flex edge can have a damping passive force and an [equality constraint](XMLreference.md) associated with it, resulting in edge constraint forces. In the latter case, passive forces are usually unnecessary. For a 1D flex, an edge can also have a passive stiffness, while `Solid` or `Membrane` first-party plugins can be used for the 2D and 3D case, respectively. which would generally make edge constraints unnecessary. However these are modeling choices left to the user. MuJoCo allows all these mechanisms to be combined as desired.


<span class="at">stiffness</span>: <span class="at-val">real(1), "0"</span>  
Stiffness of all edges. Only for 1D flex. Integrated explicitly; not supported by the [discrete](XMLreference.md) integrator (use [elasticity](XMLreference.md) or [edge equality](XMLreference.md) instead).



<span class="at">damping</span>: <span class="at-val">real(1), "0"</span>  
Damping of all edges. Integrated explicitly; not supported by the [discrete](XMLreference.md) integrator (use [elasticity/damping](XMLreference.md) instead).


##### <span class="el-prefix">flex/</span> ⁠ **elasticity** `dot`

**2D and 3D flexes** use a [Saint Venant-Kirchhoff](https://en.wikipedia.org/wiki/Hyperelastic_material#Saint_Venant%E2%80%93Kirchhoff_model) model discretized with piecewise linear finite elements, intended to simulate the compression or elongation of hyperelastic materials subjected to large displacements (finite rotations) and small strains, since it uses a nonlinear strain-displacement but a linear stress-strain relationship. See also [deformable](modeling.md) objects and [this model](https://github.com/google-deepmind/mujoco/blob/main/model/flex/floppy.xml).

For 3D flexes, the stretching energy density is $`\mu \, \textrm{tr}(\varepsilon^2) + \frac{\lambda}{2}
\textrm{tr}(\varepsilon)^2`$, where $`\varepsilon`$ is the Green strain and $`\mu = E / (2 (1 + \nu))`$, $`\lambda = E \nu / ((1 + \nu) (1 - 2 \nu))`$ are the Lamé parameters given by [young](XMLreference.md) $`E`$ and [poisson](XMLreference.md) $`\nu`$. For 2D flexes (shells of [thickness](XMLreference.md) $`t`$), the stretching (membrane) energy per unit area is $`t`$ times the same density with the plane-stress parameter $`\lambda^* = E \nu / (1 - \nu^2)`$ instead of $`\lambda`$. The bending energy of 2D flexes is a discrete hinge model for flat references, normalized so that bending a flat sheet into a cylinder of curvature $`\kappa`$ stores the Kirchhoff plate energy $`D \kappa^2 / 2`$ per unit area, with bending rigidity $`D = E t^3 / (12 (1 - \nu^2))`$. Poisson's ratio enters the bending energy only through $`D`$.

**1D flexes** are [discrete elastic rods](https://www.cs.columbia.edu/cg/pdfs/143-rods.pdf) with bending and torsion and cross-section given by [section](XMLreference.md) (see [Rods](modeling.md) for details):

- **Bending:** Every interior vertex shared by two edges of reference lengths $`\ell_0, \ell_1`$ stores bending energy $`k |\kappa b - \kappa b_0|^2`$ with stiffness $`k = E I / (\ell_0 + \ell_1)`$, where $`\kappa b`$ is the discrete curvature binormal and $`I`$ is the second moment of area of the cross-section. Vertices bent by more than $`10^{-4}`$ rad in `qpos0` keep their reference curvature $`\kappa b_0`$ (so curved rods such as rings or arcs are at rest in `qpos0`); for an isolated curved vertex on a twistless circular rod, only the curvature magnitude $`|\kappa b_0|`$ is held and its bending plane is free. Less-bent vertices are treated as straight ($`\kappa b_0 = 0`$); to start a straight rod in a bent or coiled pose with stored energy, set `qpos` or use a [keyframe](XMLreference.md).
- **Torsion:** Each vertex of a single-hinge chain has torsional stiffness $`k_t = G J / (\ell_0 + \ell_1)`$, while pairs of adjacent curved vertices on closed circular loops (or raw `<flex dim="1">` chains without twist joints) penalize the dihedral twist of their osculating planes across the shared edge of length $`\ell_1`$ with stiffness $`k_d = G J / (2 \ell_1)`$. Here $`G`$ is the shear modulus from [shear](XMLreference.md) or $`G = E / (2 (1 + \nu))`$ when <span class="at">shear</span> is zero, and $`J`$ is the Saint-Venant torsional constant of the cross-section.
- **Per-edge twist joints and clamped vs. free ends:** For open-chain 1D elastic rods with $`n \ge 2`$ edges (both **circle** and **box** [sections](XMLreference.md)), [flexcomp](XMLreference.md) creates per-edge twist bodies and hinge joints `<name>_twist_0`, ..., `<name>_twist_{n-2}`, `<name>_twist` parented to the world body, with per-edge polar mass moment of inertia ($`\frac{1}{2} m_e r^2`$ for **circle** and $`\frac{1}{3} m_e (a^2 + b^2)`$ for **box** half-sizes $`a, b`$) and frame-indifferent relative Rayleigh torsional damping. An edge whose two points are pinned is clamped: the first edge with `<pin id="0 1"/>`, or the last edge when the last two points of a rod with $`n \ge 3`$ edges are pinned. A clamped edge has no twist joint (`<name>_twist_0` or `<name>_twist` is omitted), and the body holding it fixes that end's material frame and receives the reaction torque of the rod. With `<pin id="0"/>` or no pin, `<name>_twist_0` remains free, and an unclamped `<name>_twist` can be actuated to twist the far end. A raw [flex](XMLreference.md) binds the hinge joints with these names: each unclamped edge needs one and, when the first edge is free, `<name>_twist_0` must immediately precede the joint of the second edge. Contact Jacobians couple frictional contact forces via their cross-sectional lever arm into each element's two vertices and edge twist DOF, including the velocity of the surface point due to the rotation of the element, enabling circular cables to roll on surfaces and twist in grippers. Because the per-edge twist DOFs have small polar inertia and stiff torsional coupling, the [discrete](XMLreference.md) integrator with the `CG` or `Newton` [solver](XMLreference.md) is recommended: it solves the tridiagonal torsional system, including the bending stiffness of each twist angle, implicitly (`PGS` is not supported with flex). Otherwise use a smaller timestep with `Euler` or `RK4`.
- **Box sections:** For <span class="at">section</span> **box** (requires a single open chain with at least two elements and per-edge twist joints, which [flexcomp](XMLreference.md) creates; a raw flex without them fails to compile), the principal bending stiffnesses $`k_{1,2} = E I_{1,2} / (\ell_0 + \ell_1)`$ are anisotropic, all interior vertices carry directional reference curvature in the material frame, and bending damping uses the geometric mean $`\sqrt{k_1 k_2}`$ on the weak axis so that the damping ratio $`\zeta_i \propto \sqrt{k_i}`$ is equalized across both principal axes. Rendering and collisions with planes, spheres, capsules, boxes, and other 1D rods use an oriented box of half-sizes [sectionsize](XMLreference.md) in the DER material frame. Against other geom types (meshes, cylinders, ellipsoids, height fields) and 2D or 3D flexes, the elements collide as capsules whose radius is the minor half-size, which the compiler assigns to <span class="at">radius</span>; an explicit <span class="at">radius</span> that differs from it is a compile error.
- **State:** In `mjData.plastic` at `flex_plasticadr[f]`, an open rod with per-edge twist joints (every box-section rod has them) stores `6 n + (n - 1)` numbers: the time-parallel reference frames `(t_old, u_old)` of its $`n`$ edges, followed by the reference twist of each interior vertex, unwrapped across steps so that the twist energy stays continuous when the rod writhes or tumbles. This is not plasticity, but state snapshots must include `mjSTATE_PLASTIC` to save and restore it. Without it (after *mj_resetData* or a keyframe without plastic state), the reference frames restart from the reference frame of the first edge (following its body when clamped, or transported from `qpos0` to the current tangent when free), propagated twist-free along the rod.
- **Limitations:** Stretching is not included; use [edge](XMLreference.md) equality constraints (or edge stiffness under integrators other than `discrete`) instead. Rod elasticity is integrated implicitly by [discrete](XMLreference.md) (using a positive semi-definite Hessian approximation) and explicitly by `Euler` and `RK4`; `implicit` and `implicitfast` are not supported, nor are [dof](XMLreference.md) **trilinear** and **quadratic**.

Flex elasticity (both standard and interpolated) supports vertices or nodes attached to articulated bodies, including jointless welded children, under both **Newton** and **CG** with the [discrete](XMLreference.md) integrator. A vertex or node pinned to a moving body follows that body's motion and applies its reaction force and torque to the body. **Newton** is fastest when every vertex and node is fixed or sits on a body with three slide joints along the world axes: their stiffness is then assembled as 3x3 vertex blocks. Once any flex in the model has another kind of attachment, the stiffness of all its flexes is pulled back through the attachment Jacobians, which costs more per step. MuJoCo Warp does not yet support articulated attachments with **Newton**; use **CG** there. Mocap attachments are not supported for non-rigid flexes with elasticity because mocap poses do not provide velocities for elastic damping, except for 1D flexes with zero [damping](XMLreference.md).


<span class="at">young</span>: <span class="at-val">real(1), "0"</span>  
Young's elastic modulus, a measure of tensile and compressive stiffness for continuum elastic materials. Units of $`\textrm{pressure}=\textrm{force}/\textrm{area}`$.



<span class="at">poisson</span>: <span class="at-val">real(1), "0"</span>  
Poisson's ratio, the ratio of transverse deformation to applied longitudinal strain. This unitless quantity is in the range $`[0, 0.5)`$. Small or large values imply compressibility or incompressiblity, respectively.



<span class="at">shear</span>: <span class="at-val">real(1), "0"</span>  
Shear modulus $`G`$ used for the torsional stiffness of 1D flexes, units of $`\textrm{pressure}=\textrm{force}/\textrm{area}`$. Must be non-negative. If zero, the isotropic value $`G = E / (2 (1 + \nu))`$ is computed from [young](XMLreference.md) and [poisson](XMLreference.md); if positive, it overrides that value. Ignored for 2D and 3D flexes.



<span class="at">damping</span>: <span class="at-val">real(1), "0"</span>  
Rayleigh's damping coefficient, units of time. This quantity scales the stiffness defined by Young's modulus to produce the damping matrix.



<span class="at">thickness</span>: <span class="at-val">real(1), "-1"</span>  
Shell thickness, units of length; only used for 2D flexes. The stretching stiffness of 2D flexes is proportional to the thickness $`t`$ and their bending stiffness to $`t^3`$, see [elasticity](XMLreference.md). This thickness can be set equal to 2 times the [radius](XMLreference.md) in order to match the geometry, but is exposed separately since the radius might be constrained by considerations related to collision detection.


[<img src="https://www.gstatic.com/mujoco/model/plastic/clay.webp" class="align-right" style="width:40.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/model/plastic/clay.xml)


<span class="at">yield</span>: <span class="at-val">real(1 or 2), "0"</span>  
Dimensionless plastic yield strain thresholds $`\varepsilon_y`$ for stretching and bending of 2D and 3D flexes. For non-interpolated 2D flexes, a single value applies to both, e.g., `yield="0.01"` is equivalent to `yield="0.01 0.01"`; for other flexes, a single value is the stretching threshold. A mode (stretching or bending) is plastic if its threshold is positive at compile time; its plastic state is then allocated in `mjData.plastic` and the bit of the mode is set in `mjModel.flex_plasticmode[f]` (1: bending, 2: stretching). A mode whose threshold is zero has no plastic state and remains purely elastic, e.g., `yield="0.01 0"` makes only stretching plastic. As for joints and tendons, setting the threshold of a plastic mode to zero at runtime in `mjModel.flex_yield` (which has two columns) corresponds to zero yield strain (full plastic flow). If the stretching (first) threshold is positive, each element's (or interpolated cell's/face's) elastic stretching strain tensor is bounded by the von Mises ($`J_2`$) yield criterion (3D isochoric in 3D, plane-stress with out-of-plane thinning in tension in 2D) via radial return mapping. If the bending (second) threshold is positive, which requires a non-interpolated 2D flex (a compiler error otherwise), for shells with bending enabled ([elastic2d](XMLreference.md) **bend** or **both**), each interior hinge's outer-fiber bending strain $`\frac{t}{2} |\Delta\kappa_e| \le \varepsilon_y`$ is bounded via return mapping in dihedral angle space (assuming an initially flat rest configuration). For example, `yield="0 0.001"` makes a shell yield in bending while its stretching remains elastic. 1D flexes do not support plasticity (both values must be zero). In `mjData.plastic` at `flex_plasticadr[f]`, a non-interpolated flex stores its stretching plastic metric offsets first (`3 * elemnum` entries in 2D or `6 * elemnum` entries in 3D when stretching is plastic), followed by `edgenum` bending plastic entries in 2D when bending is plastic. An interpolated flex with [cellcount](XMLreference.md) $`(c_x, c_y, c_z)`$ stores one dimensionless plastic stretching strain per grid cell (`6 * cx * cy * cz` entries in 3D) or per outer grid face in 2D shell mode (`3 * 2 * (cy*cz + cx*cz + cx*cy)` entries); the elastic strain is measured in the corotated frame of the polar decomposition of the physical deformation gradient $`J_e = \partial x / \partial X`$. Bending plasticity is not supported for interpolated flexes: with [elastic2d](XMLreference.md) **bend**, <span class="at">yield</span> is ignored and the flex remains purely elastic. See [model/plastic/](https://github.com/google-deepmind/mujoco/tree/main/model/plastic/) for example models.



<span class="at">elastic2d</span>: <span class="at-val">\[none, bend, stretch, both\], "none"</span>  
Elastic contribution to passive forces of 2D flexes. "none": none, "bend": bending only, "stretch": stretching only, "both": bending and stretching. Bending is not yet supported by [dof](XMLreference.md) **trilinear** and **quadratic**.



<span class="at">section</span>: <span class="at-val">\[circle, box\], "circle"</span>  
Cross-section of 1D flexes, used to compute the second moments of area $`I_1, I_2`$ and torsional constant $`J`$ of the bending and torsional stiffnesses. "circle": $`I_1 = I_2 = \pi r^4 / 4`$ and $`J = \pi r^4 / 2`$, where $`r`$ is the flex [radius](XMLreference.md). "box": rectangle with half-sizes given by [sectionsize](XMLreference.md) and full sizes $`w, h`$, with principal second moments $`I_1 = h w^3 / 12`$, $`I_2 = w h^3 / 12`$, and Saint-Venant torsional constant $`J`$ (requires an open chain). Both rendering and collision detection use an oriented box of half-sizes [sectionsize](XMLreference.md) in the DER material frame when <span class="at">section</span> is "box" and a capsule of the flex radius otherwise.



<span class="at">sectionsize</span>: <span class="at-val">real(2), "0 0"</span>  
Half-sizes of the "box" cross-section of 1D flexes, units of length. Both values must be positive when [section](XMLreference.md) is "box"; ignored otherwise. With a "box" section the flex radius is set to the minor half-size, so <span class="at">radius</span> must be omitted or equal to it.


##### <span class="el-prefix">flex/</span> ⁠ **contact** `dot`

This element adjusts the contact properties of the flex. It is mostly identical to geom contact properties, with some extensions specific to flexes.


<span class="at">selfcollide</span>: <span class="at-val">\[none, narrow, bvh, sap, auto\], "auto"</span>  
This determines the strategy for midphase collision pruning of element pairs belonging to the same flex. **none** means flex elements cannot collide with each other. **narrow** means narrow phase only (i.e. all pairs are checked). This is a diagnostic tool and is never a good idea in practice. **bvh** and **sap** refer to bounding volume hierarchies and sweep-and-prune (which are two different strategies for midphase collision pruning). **auto** selects **sap** in 1D and 2D, and **bvh** in 3D. Which strategy performs better depends on the specifics of the model. The automatic setting is just a simple rule which we have found to perform well in general.

For interpolated flexes (**trilinear** or **quadratic** [dofs](XMLreference.md)), elements in the same or neighboring [cells](XMLreference.md) do not self-collide, so self-collision requires at least 3 cells along an axis; **auto** prunes non-neighboring cell pairs by their bounding boxes before testing element pairs.



<span class="at">activelayers</span>: <span class="at-val">int(1), "1"</span>  
This only has an effect for 3D flexes. Each tetrahedron is labeled by the model compiler with an integer corresponding to (graph) distance to the outside surface of the flex. Thus outside-facing elements are in layer 0, their neighbors are in layer 1, etc. This attribute specifies how many layers will be allowed to participate in collisions. The default setting 1 means that only one layer (i.e. layer 0) can collide, with itself and with the rest of the world. This is usually sufficient, however if the outer layer is composed of small tetrahedra, another body can "pierce" it and get stuck. In that case the value should be increased.






















<span class="at">contype</span>, <span class="at">conaffinity</span>, <span class="at">condim</span>, <span class="at">priority</span>, <span class="at">friction</span>, <span class="at">solmix</span>, <span class="at">solref</span>, <span class="at">solimp</span>, <span class="at">margin</span>, <span class="at">gap</span>  
Same meaning as regular [geom](XMLreference.md) attributes.


<span class="at">passive</span>: <span class="at-val">\[true, false\], "false"</span>  
When enabled, contact of this flex with another flex, with itself, or with static geometry is not added to the contact solver and is instead applied as a passive normal force. Contact with a body that can move is left on the constraint solver.

Friction is not modelled on this path: every passive contact is frictionless (condim 1) regardless of the specified condim, and the force is purely normal. A flex therefore slides freely over static geometry, so a cloth will not stay draped over a fixed shape and will not come to rest on a slope. Where friction matters more than non-penetration, leave this option off.

The force is a penalty on penetration depth whose stiffness is chosen as a natural frequency scaled by the participating vertex mass (or for interpolated flexes, the effective cage node mass at the contact point scaled by the node-to-vertex ratio), so a single value is appropriate across model scales and mesh resolutions; it is not user-specified. That stiffness is integrated implicitly, its curvature being carried by the effective metric, and is therefore far stiffer than an explicit force at the same timestep could be. It follows that the feature requires the `discrete` [integrator](XMLreference.md), with the `CG` or `Newton` [solver](XMLreference.md), no [noslip](XMLreference.md) iterations and the [sleep](XMLreference.md) flag disabled. A model requesting passive flex collisions otherwise is rejected with an error.

Being a penalty force, it does not guarantee non-penetration: a thin flex moving fast enough to cross another within one step will pass through it. This is an experimental feature.


#### <span class="el-prefix">deformable/</span> ⁠ **skin** ​

These are deformable meshes whose vertex positions and normals are computed each time the model is rendered. MuJoCo skins are only used for visualization and do not affect the physics in any way. In particular, collisions involve the geoms of the bodies to which the skin is attached, and not the skin itself. Unlike regular meshes which are referenced from geoms and participate in collisions, the skin is not referenced from anywhere else in the model. It is a stand-alone element that is used by renderer and not by the simulator.

The skin has vertex positions and normals updated at runtime, and triangle faces and optional texture coordinates which are predefined. It also has "bones" used for updating. Bones are regular MuJoCo bodies referenced with the <span class="el">bone</span> subelement. Each bone has a list of vertex indices and corresponding real-valued weights which specify how much the bone position and orientation influence the corresponding vertex. The vertex has local coordinates with respect to every bone that influences it. The local coordinates are computed by the model compiler, given global vertex coordinates and global bind poses for each body. The bind poses do not have to correspond to the model reference configuration qpos0. Note that the vertex positions and bone bind poses provided in the skin definition are always global, even if the model itself is defined in local coordinates.

At runtime the local coordinates of each vertex with respect to each bone that influences it are converted to global coordinates, and averaged in proportion to the corresponding weights to obtain a single set of 3D coordinates for each vertex. Normals then are computed automatically given the resulting global vertex positions and face information. Finally, the skin can be inflated by applying an offset to each vertex position along its (computed) normal. Skins are one-sided for rendering purposes; this is because back-face culling is needed to avoid shading and aliasing artifacts. When the skin is a closed 3D shape this does not matter because the back sides cannot be seen. But if the skin is a 2D object, we have to specify both sides and offset them slightly to avoid artifacts.

Similar to meshes, skins can be specified directly in the XML via attributes documented later, or loaded from a binary SKN file which is in a custom format. The specification of skins is more complex than meshes because of the bone subelements. The file format starts with a header of 4 integers: nvertex, ntexcoord, nface, nbone. The first three are the same as in meshes, and specify the total number of vertices, texture coordinate pairs, and triangle faces in the skin. ntexcoord can be zero or equal to nvertex. nbone specifies the number of MuJoCo bodies that will be used as bones in the skin. The header is followed by the vertex, texcoord and face data, followed by a specification for each bone. The bone specification contains the name of the corresponding model body, 3D bind position, 4D bind quaternion, number of vertices influenced by the bone, and the vertex index array and weight array. Body names are represented as fixed-length character arrays and are expected to be 0-terminated. Characters after the first 0 are ignored. The contents of the SKN file are:

``` Text
(int32)   nvertex
(int32)   ntexcoord
(int32)   nface
(int32)   nbone
(float)   vertex_positions[3*nvertex]
(float)   vertex_texcoords[2*ntexcoord]
(int32)   face_vertex_indices[3*nface]
for each bone:
    (char)    body_name[40]
    (float)   bind_position[3]
    (float)   bind_quaternion[4]
    (int32)   vertex_count
    (int32)   vertex_index[vertex_count]
    (float)   vertex_weight[vertex_count]
```

Similar to the other custom binary formats used in MuJoCo, the file size in bytes is strictly enforced by the model compiler. The skin file format has subelements so the overall file size formula is difficult to write down, but should be clear from the above specification.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the skin.



<span class="at">file</span>: <span class="at-val">string, optional</span>  
The SKN file from which the skin will be loaded. The path is determined as described in the meshdir attribute of [compiler](XMLreference.md). If the file is omitted, the skin specification must be provided in the XML using the attributes below.



<span class="at">vertex</span>: <span class="at-val">real(3\*nvert), optional</span>  
Vertex 3D positions, in the global bind pose where the skin is defined.



<span class="at">texcoord</span>: <span class="at-val">real(2\*nvert), optional</span>  
Vertex 2D texture coordinates, between 0 and 1. Note that skin and geom texturing are somewhat different. Geoms can use automated texture coordinate generation while skins cannot. This is because skin data are computed directly in global coordinates. So if the material references a texture, one should specify explicit texture coordinates for the skin using this attribute. Otherwise the texture will appear to be stationary in the world while the skin moves around (creating an interesting effect but probably not as intended).



<span class="at">face</span>: <span class="at-val">int(3\*nface), optional</span>  
Triangular skin faces. Each face is a triple of vertex indices, which are integers between zero and nvert-1.



<span class="at">inflate</span>: <span class="at-val">real, "0"</span>  
If this number is not zero, the position of vertex during updating will be offset along the vertex normal, but the distance specified in this attribute. This is particularly useful for skins representing flexible 2D shapes.



<span class="at">material</span>: <span class="at-val">string, optional</span>  
If specified, this attribute applies a material to the skin.



<span class="at">rgba</span>: <span class="at-val">real(4), "0.5 0.5 0.5 1"</span>  
Instead of creating material assets and referencing them, this attribute can be used to set color and transparency only. This is not as flexible as the material mechanism, but is more convenient and is often sufficient. If the value of this attribute is different from the internal default, it takes precedence over the material.



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
Integer group to which the skin belongs. This attribute can be used for custom tags. It is also used by the visualizer to enable and disable the rendering of entire groups of skins.


##### <span class="el-prefix">skin/</span> ⁠ **bone** ​

This element defines a bone of the skin. The bone is a regular MuJoCo body which is referenced by name here.


<span class="at">body</span>: <span class="at-val">string, required</span>  
Name of the body corresponding to this bone.



<span class="at">bindpos</span>: <span class="at-val">real(3), required</span>  
Global body position corresponding to the bind pose.



<span class="at">bindquat</span>: <span class="at-val">real(4), required</span>  
Global body orientation corresponding to the bind pose.



<span class="at">vertid</span>: <span class="at-val">int(nvert), required</span>  
Integer indices of the vertices influenced by this bone. The vertex index corresponds to the order of the vertex in the skin mesh. The number of vertex indices specified here (nvert) must equal the number of vertex weights specified with the next attribute. The same vertex may be influenced by multiple bones, and each vertex must be influenced by at least one bone.



<span class="at">vertweight</span>: <span class="at-val">real(nvert), required</span>  
Weights for the vertices influenced by this bone, in the same order as the vertex indices. Negative weights are allowed (which is needed for cubic interpolation for example) however the sum of all bone weights for a given vertex must be positive.


### **equality** ​

This is a grouping element for equality constraints. It does not have attributes. See the [Equality](computation/index.md) section of the Computation chapter for a detailed description of equality constraints. Several attributes are common to all equality constraint types, thus we document them only once, under the [connect](XMLreference.md) element.

#### <span class="el-prefix">equality/</span> ⁠ **connect** ​

This element creates an equality constraint that connects two bodies at a point. The constraint effectively defines a ball joint outside the kinematic tree. Connect constraints can be specified in one of two ways

- Using [body1](XMLreference.md) and [anchor](XMLreference.md) (both required) and optionally [body2](XMLreference.md). When using this specification, the constraint is assumed to be satisfied at the configuration in which the model is defined (`mjData.qpos0`).
- [site1](XMLreference.md) and [site2](XMLreference.md) (both required). When using this specification, the two sites will be pulled together by the constraint, regardless of their position in the default configuration. An example of this specification is shown in [this model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/equality_site.xml).


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the equality constraint.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">active</span>: <span class="at-val">\[false, true\], "true"</span>  
If this attribute is set to "true", the constraint is active and the constraint solver will try to enforce it. The field [mjModel.eq_active0](APIreference/APItypes.md) corresponds to this value, and is used to initialize [mjData.eq_active](APIreference/APItypes.md), which is user-settable at runtime.




<span class="at">solref</span>, <span class="at">solimp</span>  
Constraint solver parameters for equality constraint simulation. See [Solver parameters](modeling.md).




<span class="at">body1</span>: <span class="at-val">string, optional</span>  
Name of the first body participating in the constraint. Either this attribute and <span class="at">anchor</span> must be specified, or <span class="at">site1</span> and <span class="at">site2</span> must be specified.



<span class="at">body2</span>: <span class="at-val">string, optional</span>  
Name of the second body participating in the constraint. If this attribute is omitted, the second body is the world body.



<span class="at">anchor</span>: <span class="at-val">real(3), optional</span>  
Coordinates of the 3D anchor point where the two bodies are connected, in the local coordinate frame of <span class="at">body1</span>. The constraint is assumed to be satisfied in the configuration at which the model is defined (`mjData.qpos0`), which lets the compiler compute the associated anchor point for <span class="at">body2</span>.



<span class="at">site1</span>: <span class="at-val">string, optional</span>  
Name of a site belonging to the first body participating in the constraint. When specified, <span class="at">site2</span> must also be specified. The (<span class="at">site1</span>, <span class="at">site2</span>) specification is a more flexible alternative to the body-based specification, and is different in two ways. First, the sites are not required to overlap at the default configuration; if they do not overlap then the sites will "snap together" at the beginning of the simulation. Second, changing the site positions in `mjModel.site_pos` at runtime will correctly change the position of the constraint (i.e. the content of `mjModel.eq_data` has no effect when this semantic is used).



<span class="at">site2</span>: <span class="at-val">string, optional</span>  
Name of a site belonging to the second body participating in the constraint. When specified, <span class="at">site1</span> must also be specified. See the [site1](XMLreference.md) description for more details.


#### <span class="el-prefix">equality/</span> ⁠ **weld** ​

This element creates a weld equality constraint. It attaches two bodies to each other, removing all relative degrees of freedom between them (softly of course, like all other constraints in MuJoCo). The two bodies are not required to be close to each other. The relative body position and orientation being enforced by the constraint solver is the one in which the model was defined. Note that two bodies can also be welded together rigidly, by defining one body as a child of the other body, without any joint elements in the child body. Weld constraints can be specified in one of two ways:

- Using [body1](XMLreference.md) (and optionally [anchor](XMLreference.md), [relpose](XMLreference.md), [body2](XMLreference.md)). When using this specification, the constraint is assumed to be satisfied at the configuration in which the model is defined.
- [site1](XMLreference.md) and [site2](XMLreference.md) (both required). When using this specification, the frames of the two sites will be aligned by the constraint, regardless of their position in the default configuration. An example of this specification is shown in [this model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/equality_site.xml).






<span class="at">name</span>, <span class="at">class</span>, <span class="at">active</span>, <span class="at">solref</span>, <span class="at">solimp</span>  
Same as in [connect](XMLreference.md) element.







<span class="at">body1</span>: <span class="at-val">string, optional</span>  
Name of the first body participating in the constraint. Either this attribute and must be specified or <span class="at">site1</span> and <span class="at">site2</span> must be specified.



<span class="at">body2</span>: <span class="at-val">string, optional</span>  
Name of the second body. If this attribute is omitted, the second body is the world body. Welding a body to the world and changing the corresponding component of mjData.eq_active at runtime can be used to fix the body temporarily.



<span class="at">relpose</span>: <span class="at-val">real(7), "0 1 0 0 0 0 0"</span>  
This attribute specifies the relative pose (3D position followed by 4D quaternion orientation) of the anchor point relative to body1. The position part (first 3 components) gives the anchor coordinates in the local frame of body1, and the quaternion part (last 4 components) gives the relative orientation of body2 relative to body1. If the quaternion part (i.e., last 4 components of the vector) are all zeros, as in the default setting, this attribute is ignored and the relative pose is the one corresponding to the model reference pose in qpos0, which *mj_setConst* recomputes; `mjModel.eq_data[11]` marks such welds. The unusual default is because all equality constraint types share the same default for their numeric parameters.



<span class="at">anchor</span>: <span class="at-val">real(3), "0 0 0"</span>  
Coordinates of the weld point relative to body2. If <span class="at">relpose</span> is not specified, the meaning of this parameter is the same as for connect constraints, except that is relative to body2. If <span class="at">relpose</span> is specified, body1 will use the pose to compute its anchor point.



<span class="at">site1</span>: <span class="at-val">string, optional</span>  
Name of a site belonging to the first body participating in the constraint. When specified, <span class="at">site2</span> must also be specified. The (<span class="at">site1</span>, <span class="at">site2</span>) specification is a more flexible alternative to the body-based specification, and is different in two ways. First, the sites are not required to overlap at the default configuration; if they do not overlap then the sites will "snap together" at the beginning of the simulation. Second, changing the site position and orientation in `mjModel.site_pos` and `mjModel.site_quat` at runtime will correctly change the position and orientation of the constraint (i.e. the content of `mjModel.eq_data` has no effect when this semantic is used, with the exception of [torquescale](XMLreference.md)).



<span class="at">site2</span>: <span class="at-val">string, optional</span>  
Name of a site belonging to the second body participating in the constraint. When specified, <span class="at">site1</span> must also be specified. See the [site1](XMLreference.md) description for more details.



<span class="at">torquescale</span>: <span class="at-val">real, "1"</span>  
A constant that scales the angular residual (angular constraint violation). Notionally in units of $`\textrm{torque}/\textrm{force}=\textrm{length}`$. Intuitively this coefficient defines how much the weld "cares" about rotational displacements vs. translational displacements. Setting this value to 0 makes the <span class="el">weld</span> behave like a <span class="el">connect</span> constraint. Note that this value has units of length and can therefore be understood as follows. Imagining that the weld is implemented by a flat patch of glue sticking the two bodies together, <span class="at">torquescale</span> can be interpreted as the diameter of this glue patch.


#### <span class="el-prefix">equality/</span> ⁠ **joint** ​

This element constrains the position or angle of one joint to be a quartic polynomial of another joint. Only scalar joint types (slide and hinge) can be used.






<span class="at">name</span>, <span class="at">class</span>, <span class="at">active</span>, <span class="at">solref</span>, <span class="at">solimp</span>  
Same as in [connect](XMLreference.md) element.







<span class="at">joint1</span>: <span class="at-val">string, required</span>  
Name of the first joint.



<span class="at">joint2</span>: <span class="at-val">string, optional</span>  
Name of the second joint. If this attribute is omitted, the first joint is fixed to a constant.



<span class="at">polycoef</span>: <span class="at-val">real(5), "0 1 0 0 0"</span>  
Coefficients $`a_0 \ldots a_4`$ of the quartic polynomial. If the joint values of <span class="at">joint1</span> and <span class="at">joint2</span> are respectively $`y`$ and $`x`$, and their reference positions (corresponding to the joint values in the initial model configuration) are $`y_0`$ and $`x_0`$, the constraint is:

``` math
y-y_0 = a_0 + a_1(x-x_0) + a_2(x-x_0)^2 + a_3(x-x_0)^3 + a_4(x-x_0)^4
```

Omitting <span class="at">joint2</span> is equivalent to setting $`x = x_0`$, in which case the constraint is $`y = y_0 + a_0`$.


#### <span class="el-prefix">equality/</span> ⁠ **tendon** ​

This element constrains the length of one tendon to be a quartic polynomial of another tendon.






<span class="at">name</span>, <span class="at">class</span>, <span class="at">active</span>, <span class="at">solref</span>, <span class="at">solimp</span>  
Same as in [connect](XMLreference.md) element.







<span class="at">tendon1</span>: <span class="at-val">string, required</span>  
Name of the first tendon.



<span class="at">tendon2</span>: <span class="at-val">string, optional</span>  
Name of the second tendon. If this attribute is omitted, the first tendon is fixed to a constant.



<span class="at">polycoef</span>: <span class="at-val">real(5), "0 1 0 0 0"</span>  
Same as in the [equality/joint](XMLreference.md) element above, but applied to tendon lengths instead of joint positions.


#### <span class="el-prefix">equality/</span> ⁠ **flex** ​

This element constrains the lengths of all edges of a specified flex to their respective lengths in the initial model configuration. In this way the edges are used to maintain the shape of the deformable entity. Note that all other equality constraint types add a fixed number of scalar constraints, while this element adds as many scalar constraints as there are edges in the specified flex. See [this model](https://github.com/google-deepmind/mujoco/blob/main/model/flex/plate.xml) for an example.






<span class="at">name</span>, <span class="at">class</span>, <span class="at">active</span>, <span class="at">solref</span>, <span class="at">solimp</span>  
Same as in [connect](XMLreference.md) element.







<span class="at">flex</span>: <span class="at-val">string, required</span>  
Name of the flex whose edges are being constrained.


#### <span class="el-prefix">equality/</span> ⁠ **flexstrain** ​

This element constrains the strain of a trilinear or quadratic flex to its initial values. For trilinear elements, a B-bar formulation is used to prevent volumetric locking: the trace of strain (I₁) and volume ratio (J-1 = det(F)-1) are constrained at the element center, while the three off-diagonal shear components (E₁₂, E₁₃, E₂₃) are constrained at each of the 8 Gauss points, giving 26 constraints per element. For quadratic elements, all 6 strain components (3 invariants + 3 shear) are constrained at each of the 27 Gauss points, giving 162 constraints per element. This constraint type is only supported for dimension 3 flexes with trilinear or quadratic interpolation. See [this model](https://github.com/google-deepmind/mujoco/blob/main/model/flex/strain.xml) for an example.

The strain constraint replaces the stretch elasticity of the flex: the compiled element stiffness holds the constraint eigenmodes instead of the [young](XMLreference.md) and [poisson](XMLreference.md) stiffness, and the passive stretch force is not computed. A positive <span class="at">young</span> is therefore rejected by the compiler unless [elastic2d](XMLreference.md) is <span class="at-val">bend</span>, in which case it only determines the bending stiffness of the shell. Note that deactivating the constraint at runtime leaves the flex without stretch elasticity; to simulate a volumetric elastic solid, remove the constraint and set <span class="at">young</span> and <span class="at">poisson</span> before compiling.






<span class="at">name</span>, <span class="at">class</span>, <span class="at">active</span>, <span class="at">solref</span>, <span class="at">solimp</span>  
Same as in [connect](XMLreference.md) element.







<span class="at">flex</span>: <span class="at-val">string, required</span>  
Name of the flex whose strain is being constrained.



<span class="at">cell</span>: <span class="at-val">int(3), optional</span>  
3D grid index (i, j, k) identifying the cell in the flex object. The grid size is specified in the [cellcount](XMLreference.md) attribute.


### **tendon** ​

Grouping element for tendon definitions. The attributes of fixed tendons are a subset of the attributes of spatial tendons, thus we document them only once under spatial tendons. Tendons can be used to impose length limits, simulate spring, damping and dry friction forces, as well as attach actuators to them. When used in equality constraints, tendons can also represent different forms of mechanical coupling.

#### <span class="el-prefix">tendon/</span> ⁠ **spatial** ​

<figure class="align-right">
<img src="images/XMLreference/tendon.png" width="400" />
</figure>

This element creates a spatial tendon, which is a minimum-length path passing through specified via-points and wrapping around specified obstacle geoms. The objects along the path are defined with the sub-elements [site](XMLreference.md) and [geom](XMLreference.md) below. One can also define [pulleys](XMLreference.md) which split the path in multiple branches. Each branch of the tendon path must start and end with a site, and if it has multiple obstacle geoms they must be separated by sites - so as to avoid the need for an iterative solver at the tendon level. This example illustrates a multi-branch tendon acting as a finger extensor, with a counter-weight instead of an actuator: [tendon.xml](_static/tendon.xml).

A second form of wrapping is where the tendon is constrained to pass *through* a geom rather than wrap around it. This is enabled automatically when a sidesite is specified and its position is inside the volume of the obstacle geom.


I2q7D0Vda-A


**Visualization:** Tendon paths are visualized as in the image above, respecting the [width](XMLreference.md), [material](XMLreference.md) and [rgba](XMLreference.md) attributes below. A special kind of visualization is used for unactuated 2-point tendons with [range](XMLreference.md) or [springlength](XMLreference.md) of the form <span class="at-val">\[0 X\]</span>, with positive X. Such tendons act like a cable, applying force only when stretched. Therefore when not stretched, they are drawn as a catenary of length X, as in the clip on the right of [this example model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/catenary.xml).


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of the tendon.



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Defaults class for setting unspecified attributes.



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
Integer group to which the tendon belongs. This attribute can be used for custom tags. It is also used by the visualizer to enable and disable the rendering of entire groups of tendons.



<span class="at">limited</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
If this attribute is "true", the length limits defined by the range attribute below are imposed by the constraint solver. If this attribute is "auto", and <span class="at">autolimits</span> is set in [compiler](XMLreference.md), length limits will be enabled if range is defined.



<span class="at">actuatorfrclimited</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
This attribute specifies whether actuator forces acting on the tendon should be clamped. See [Force limits](modeling.md) for details. This attribute interacts with the [actuatorfrcrange](XMLreference.md) attribute. If this attribute is "false", actuator force clamping is disabled. If it is "true", actuator force clamping is enabled. If this attribute is "auto", and <span class="at">autolimits</span> is set in [compiler](XMLreference.md), actuator force clamping will be enabled if <span class="at">actuatorfrcrange</span> is defined.



<span class="at">range</span>: <span class="at-val">real(2), "0 0"</span>  
Range of allowed tendon lengths. Setting this attribute without specifying <span class="at">limited</span> is an error, unless <span class="at">autolimits</span> is set in [compiler](XMLreference.md).



<span class="at">actuatorfrcrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping total actuator forces acting on this tendon. See [Force limits](modeling.md) for details; to limit several commands of one physical actuator, prefer a single multi-input actuator such as [pid](XMLreference.md) with [forcerange](XMLreference.md). The compiler expects the lower bound to be nonpositive and the upper bound to be nonnegative. <br/> Setting this attribute without specifying <span class="at">actuatorfrclimited</span> is an error if <span class="at">compiler-autolimits</span> is "false".




<span class="at">solreflimit</span>, <span class="at">solimplimit</span>  
Constraint solver parameters for simulating tendon limits. See [Solver parameters](modeling.md).





<span class="at">solreffriction</span>, <span class="at">solimpfriction</span>  
Constraint solver parameters for simulating dry friction in the tendon. See also [Friction](modeling.md).




<span class="at">margin</span>: <span class="at-val">real, "0"</span>  
The limit constraint becomes active when the absolute value of the difference between the tendon length and either limit of the specified range falls below this margin. Similar to contacts, the margin parameter is subtracted from the difference between the range limit and the tendon length. The resulting constraint distance is always negative when the constraint is active. This quantity is used to compute constraint impedance as a function of distance, as explained in [Solver parameters](modeling.md).



<span class="at">frictionloss</span>: <span class="at-val">real, "0"</span>  
Friction loss caused by dry friction. To enable friction loss, set this attribute to a positive value.



<span class="at">width</span>: <span class="at-val">real, "0.003"</span>  
Radius of the cross-section area of the spatial tendon, used for rendering. Parts of the tendon that wrap around geom obstacles are rendered with reduced width.



<span class="at">material</span>: <span class="at-val">string, optional</span>  
Material used to set the appearance of the tendon.



<span class="at">rgba</span>: <span class="at-val">real(4), "0.5 0.5 0.5 1"</span>  
Color and transparency of the tendon. When this value is different from the internal default, it overrides the corresponding material properties. If a <span class="at">material</span> is unspecified and <span class="at">rgba</span> has the default value, limited tendons whose length exceeds the limit are recolored using the value of the [constraint impedance](computation/index.md) $`d`$ to mix the default color and [rgba/constraint](XMLreference.md).



<span class="at">springlength</span>: <span class="at-val">real(2), "-1 -1"</span>  
Spring resting position, can take either one or two values. If one value is given, it corresponds to the length of the tendon at rest. If it is `-1`, the tendon resting length is determined by the compiler from the spring reference configuration in `mjModel.qpos_spring`. <br/> Note that the default value of `-1`, which invokes the automatic length computation, was designed with [spatial](XMLreference.md) tendons in mind, which can only have nonegative length. In order to set the <span class="at">springlength</span> of a [fixed](XMLreference.md) tendon to `-1`, use a nearby value like `-0.99999`. <br/> If two non-decreasing values are given, they define a [dead-band](https://en.wikipedia.org/wiki/Deadband) range. If the tendon length is between the two values, the force is 0. If it is outside this range, the force behaves like a regular spring, with the rest-point corresponding to the nearest <span class="at">springlength</span> value. A deadband can be used to define tendons whose limits are enforced by springs rather than constraints.




aKa3ZlEF9_Y



<span class="at">stiffness</span>: <span class="at-val">real, "0 0 0"</span>  
Tendon stiffness coefficients $`a, b, c`$. A positive $`a`$ generates a linear spring force $`f(x) = -a x`$, acting along the tendon. Here $`x`$ is the tendon displacement defined by [springlength](XMLreference.md).

If the optional second and third components are set, they define a nonlinear polynomial spring force $`f(x) = -(a x + b x^2 + c x^3)`$. See [Polynomial forces](computation/index.md) for details.

The clip on the right is of [this model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/passive/poly_stiffness.xml).


<span class="at">springyield</span>: <span class="at-val">real, "0"</span>  
Elastic yield threshold for the tendon spring. When positive, the tendon spring reference range is allocated in the mutable state vector `mjData.plastic` at offset `mjModel.tendon_plasticadr[i]` (2 entries, initialized from `mjModel.tendon_lengthspring`) and shifts permanently whenever the displacement outside the spring deadband exceeds `springyield` (ideal elasto-plasticity). For unilateral slack tendons with `springlength="0 L"` (`L > 0`), tensile yielding shifts only the upper bound `L` while keeping the lower bound pinned at `0`. When `0` (default), plasticity is disabled (`mjModel.tendon_plasticadr[i] == -1`) and the spring is purely elastic; setting `mjModel.tendon_springyield[i] = 0` at runtime on an already-plastic tendon (`tendon_plasticadr[i] >= 0`) corresponds to zero yield threshold (full plastic slip).



<span class="at">damping</span>: <span class="at-val">real, "0 0 0"</span>  
Damping coefficients $`a, b, c`$. A positive $`a`$ produces the standard dissipative linear damping force $`f(v) = -a v`$.

If the optional second and third components are set, they define a nonlinear polynomial damping force $`f(v) = -(a v + b v |v| + c v^3)`$. Note the anti-symmetrization of the quadratic term, ensuring that the force is an odd function of velocity. See [Polynomial forces](computation/index.md) for details.


[<img src="images/XMLreference/tendon_armature.gif" class="only-light only-lightalign-right" style="width:30.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/core_smooth/ten_armature_1_compare.xml)

[<img src="images/XMLreference/tendon_armature_dark.gif" class="only-dark only-darkalign-right" style="width:30.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/core_smooth/ten_armature_1_compare.xml)


<span class="at">armature</span>: <span class="at-val">real, "0"</span>  
Inertia associated with changes in tendon length. Setting this attribute to a positive value $`m`$ adds a kinetic energy term $`\frac{1}{2}mv^2`$, where $`v`$ is the tendon velocity. Tendon inertia is most valuable when modeling the [armature](XMLreference.md) inertia in a linear actuator which contains a spinning element or the inertial motion of a fluid in a linear hydraulic actuator. In the illustration, we compare (*left*) a 3-dof system with a "tendon" implemented with a rotational joint and a slider joint with [armature](XMLreference.md), attached to the world with a [connect](XMLreference.md) constraint and (*right*) an equivalent 1-dof model with an armature-bearing tendon. Like joint [armature](XMLreference.md), this added inertia is only associated with changes in tendon length, and would not affect the dynamics of a moving fixed-length tendon. Because the tendon Jacobian $`J`$ is position-dependent, tendon armature leads to an additional bias-force term $`c = m J \dot{J}^T \dot{q}`$.



<span class="at">user</span>: <span class="at-val">real(nuser_tendon), "0 0 ..."</span>  
See [User parameters](modeling.md).


##### <span class="el-prefix">spatial/</span> ⁠ **site** ​

This attribute specifies a site that the tendon path has to pass through. Recall that sites are rigidly attached to bodies.


<span class="at">site</span>: <span class="at-val">string, required</span>  
The name of the site that the tendon must pass through.


##### <span class="el-prefix">spatial/</span> ⁠ **geom** ​

This element specifies a geom that acts as an obstacle for the tendon path. If the minimum-length path does not touch the geom it has no effect; otherwise the path wraps around the surface of the geom. Wrapping is computed analytically, which is why we restrict the geom types allowed here to spheres and cylinders. The latter are treated as having infinite length for tendon wrapping purposes. If a sidesite is defined, and its position is inside the geom, then the tendon is constrained to pass through the geom instead of passing around it.


<span class="at">geom</span>: <span class="at-val">string, required</span>  
The name of a geom that acts as an obstacle for the tendon path. Only sphere and cylinder geoms can be referenced here.



<span class="at">sidesite</span>: <span class="at-val">string, optional</span>  
To prevent the tendon path from snapping from one side of the geom to the other as the model configuration varies, the user can define a preferred "side" of the geom. The tendon then goes around the geom the same way as the path from the first endpoint $`p_1`$, through the side site $`s`$ (projected onto the surface of the geom), to the second endpoint $`p_2`$. If the straight segment between the endpoints already passes the geom that way, the tendon does not wrap. Formally, the tendon is the shortest path from $`p_1`$ to $`p_2`$ that is homotopic to the polyline $`p_1 \to s \to p_2`$ in the wrapping plane with the geom removed, i.e., that has the same winding angle around the geom center. In the images below, the side site is green and the polyline is the thin grey line.

<img src="images/XMLreference/sidesite_homotopy_light.svg" class="only-light only-lightalign-center" style="width:90.0%" alt="image" />

<img src="images/XMLreference/sidesite_homotopy_dark.svg" class="only-dark only-darkalign-center" style="width:90.0%" alt="image" />

The tendon snaps off the geom when an endpoint crosses the ray opposite the side site, so side sites should be placed such that the endpoints do not cross this ray over the range of motion, typically near the middle of the wrapped arc. Specifying a side site is often needed in practice. If the side site is inside the geom, the tendon is constrained to pass through the interior of the geom.


##### <span class="el-prefix">spatial/</span> ⁠ **pulley** ​

This element starts a new branch in the tendon path. The branches are not required to be connected spatially. Similar to the transmissions described in the [Actuation model](computation/index.md) section of the Computation chapter, the quantity that affects the simulation is the tendon length and its gradient with respect to the joint positions. If a spatial tendon has multiple branches, the length of each branch is divided by the divisor attribute of the pulley element that started the branch, and added up to obtain the overall tendon length. This is why the spatial relations among branches are not relevant to the simulation. The [tendon.xml](_static/tendon.xml) example above illustrated the use of pulleys.


<span class="at">divisor</span>: <span class="at-val">real, required</span>  
The length of the tendon branch started by the pulley element is divided by the value specified here. For a physical pulley that splits a single branch into two parallel branches, the common branch would have divisor value of 1 and the two branches following the pulley would have divisor values of 2. If one of them is further split by another pulley, each new branch would have divisor value of 4 and so on. Note that in MJCF each branch starts with a pulley, thus a single physical pulley is modeled with two MJCF pulleys. If no pulley elements are included in the tendon path, the first and only branch has divisor value of 1.


#### <span class="el-prefix">tendon/</span> ⁠ **fixed** ​

This element creates an abstract tendon whose length is defined as a linear combination of joint positions. Recall that the tendon length and its gradient are the only quantities needed for simulation. Thus we could define any scalar function of joint positions, call it "tendon", and use it in MuJoCo. The only such function supported is a fixed linear combination. The attributes of fixed tendons are a subset of the attributes of spatial tendons and have the same meaning as above.







































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">limited</span>, <span class="at">range</span>, <span class="at">solreflimit</span>, <span class="at">solimplimit</span>, <span class="at">solreffriction</span>, <span class="at">solimpfriction</span>, <span class="at">frictionloss</span>, <span class="at">margin</span>, <span class="at">springlength</span>, <span class="at">stiffness</span>, <span class="at">springyield</span>, <span class="at">damping</span>, <span class="at">user</span>  
Same as in the [spatial](XMLreference.md) element.

##### <span class="el-prefix">fixed/</span> ⁠ **joint** ​

This element adds a joint to the computation of the fixed tendon length. The position or angle of each included joint is multiplied by the corresponding coef value, and added up to obtain the tendon length.


<span class="at">joint</span>: <span class="at-val">string, required</span>  
Name of the joint to be added to the fixed tendon. Only scalar joints (slide and hinge) can be referenced here.



<span class="at">coef</span>: <span class="at-val">real, required</span>  
Scalar coefficient multiplying the position or angle of the specified joint.


### **actuator** ​

This is a grouping element for actuator definitions. Recall the discussion of MuJoCo's [Actuation model](computation/index.md) in the Computation chapter, and the [Actuator shortcuts](modeling.md) discussed earlier in this chapter. The first 13 attributes of all actuator-related elements below are the same, so we document them only once, under the <span class="el">general</span> actuator.

#### <span class="el-prefix">actuator/</span> ⁠ **general** ​

This element creates a general actuator, providing full access to all actuator components and allowing the user to specify them independently.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Element name. See [Naming elements](modeling.md).



<span class="at">class</span>: <span class="at-val">string, optional</span>  
Active defaults class. See [Default settings](modeling.md).



<span class="at">group</span>: <span class="at-val">int, "0"</span>  
Integer group to which the actuator belongs. This attribute can be used for custom tags. It is also used by the visualizer to enable and disable the rendering of entire groups of actuators.



<span class="at">nsample</span>: <span class="at-val">int, "0"</span>  
If greater than 0, this attribute creates a time-indexed ring buffer with <span class="at">nsample</span> samples of this actuator's `ctrl` history. During state advancement, the current control input is appended to the buffer with timestamp `time`, and the oldest sample is removed. Values in the history buffer can be read via *mj_readCtrl*.

A positive <span class="at-val">nsample</span> is required for [delay](XMLreference.md). See [Delays](modeling.md) for details.



<span class="at">interp</span>: <span class="at-val">\[zoh, linear, cubic\], "zoh"</span>  
The interpolation method used when reading from the history buffer. Corresponds to the `interp` argument in *mj_readCtrl*.

- `zoh`: Zero-order hold (piecewise constant).
- `linear`: Piecewise linear interpolation.
- `cubic`: Cubic spline interpolation (Catmull-Rom).

The <span class="at">interp</span> value is for advanced use-cases, see [Delays](modeling.md) for details.



<span class="at">delay</span>: <span class="at-val">real, "0"</span>  
If greater than 0, then during the forward dynamics, instead of reading the control input to the actuator from `mjData.ctrl`, the control input is read from the history buffer using *mj_readCtrl*. Requires a history buffer ([nsample](XMLreference.md) \> 0).

In the most common case, `delay = nsample * timestep`.



<span class="at">ctrllimited</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
If true, the control input to this actuator is automatically clamped to <span class="at">ctrlrange</span> at runtime. If false, control input clamping is disabled. If "auto" and <span class="at">autolimits</span> is set in [compiler](XMLreference.md), control clamping will automatically be set to true if <span class="at">ctrlrange</span> is defined without explicitly setting this attribute to "true". Note that control input clamping can also be globally disabled with the <span class="at">clampctrl</span> attribute of [option/flag](XMLreference.md).



<span class="at">forcelimited</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
If true, the force output of this actuator is automatically clamped to <span class="at">forcerange</span> at runtime. If false, force clamping is disabled. If "auto" and <span class="at">autolimits</span> is set in [compiler](XMLreference.md), force clamping will automatically be set to true if <span class="at">forcerange</span> is defined without explicitly setting this attribute to "true".



<span class="at">actlimited</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
If true, the internal state (activation) associated with this actuator is automatically clamped to <span class="at">actrange</span> at runtime. If false, activation clamping is disabled. If "auto" and <span class="at">autolimits</span> is set in [compiler](XMLreference.md), activation clamping will automatically be set to true if <span class="at">actrange</span> is defined without explicitly setting this attribute to "true". See the [Activation clamping](modeling.md) section for more details.



<span class="at">ctrlrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping the control input. The first value must be smaller than the second value. <br/> Setting this attribute without specifying <span class="at">ctrllimited</span> is an error if <span class="at">autolimits</span> is "false" in [compiler](XMLreference.md).



<span class="at">forcerange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping the force output. The first value must be no greater than the second value. On [orientation](XMLreference.md) actuators the force is a 3D torque, clamped on its norm: the second value bounds the torque magnitude and the first value must be 0. <br/> Setting this attribute without specifying <span class="at">forcelimited</span> is an error if <span class="at">autolimits</span> is "false" in [compiler](XMLreference.md).



<span class="at">actrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping the activation state. The first value must be no greater than the second value. See the [Activation clamping](modeling.md) section for more details. <br/> Setting this attribute without specifying <span class="at">actlimited</span> is an error if <span class="at">autolimits</span> is "false" in [compiler](XMLreference.md).



<span class="at">lengthrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range of feasible lengths of the actuator's transmission. See [Length Range](modeling.md).



<span class="at">gear</span>: <span class="at-val">real(6), "1 0 0 0 0 0"</span>  
This attribute scales the length (and consequently moment arms, velocity and force) of the actuator, for all transmission types. It is different from the gain in the force generation mechanism, because the gain only scales the force output and does not affect the length, moment arms and velocity. For actuators with scalar transmission, only the first element of this vector is used. The remaining elements are needed for joint, jointinparent and site transmissions where this attribute is used to specify 3D force and torque axes.



<span class="at">damping</span>: <span class="at-val">real(3), "0 0 0"</span>  
Viscous damping coefficients, contributed by the actuator to its transmission target (joint or tendon only). The damping value is scaled by [gear](XMLreference.md) squared, because the gear ratio scales both forces and velocities, leading to reflected damping (analogous to [reflected inertia](XMLreference.md)). Like [joint damping](XMLreference.md), coefficients correspond to linear, quadratic and cubic velocity. See [Polynomial forces](computation/index.md) for details.

Several actuator shortcuts have a <span class="at">kv</span> attribute which maps to [-biasprm\[2\]](XMLreference.md) and has similar semantics to <span class="at">damping</span>: (e.g., [position/kv](XMLreference.md)). The differences between these attributes are:

- <span class="at">damping</span> is applied at the transmission target, and therefore includes the gear<sup>2</sup> factor. This factor is not required for <span class="at">kv</span> as it is already applied in actuator space (so the units are identical).
- Implicit integration works for <span class="at">damping</span> when using the Euler integrator but not for <span class="at">kv</span>. To get implicit integration for <span class="at">kv</span>, implicit or implicitfast is required, see [Integrators](computation/index.md).
- <span class="at">damping</span> allows for polynomial damping, while <span class="at">kv</span> is only linear.
- Damping forces generated by <span class="at">kv</span> are subject to [forcerange](XMLreference.md) clamping, but forces generated by <span class="at">damping</span> are not.

Finally, note that while it is permitted for nonzero damping and [armature](XMLreference.md) to be specified for multiple actuators acting on the same transmission target, it is more performant to specify them for only one actuator. Since these values are summed anyway, it is recommended to place all damping and armature for one transmission target in a single actuator definition.



<span class="at">armature</span>: <span class="at-val">real, "0"</span>  
Armature inertia (or mass for slider joints) contributed by the actuator to its transmission target (joint or tendon only). This is the actual inertia of the spinning element inside the actuator (e.g., a rotor). The contributed value is scaled by [gear](XMLreference.md) squared, because the gear ratio scales both forces and velocities, leading to reflected inertia. See [joint](XMLreference.md) and [tendon](XMLreference.md) armature for more details.

See also the note in [damping](XMLreference.md) regarding multiple actuators acting on the same transmission target.



<span class="at">cranklength</span>: <span class="at-val">real, "0"</span>  
Used only for the slider-crank transmission type. Specifies the length of the connecting rod. The compiler expects this value to be positive when a slider-crank transmission is present.



<span class="at">joint</span>: <span class="at-val">string, optional</span>  
This and the next four attributes determine the type of actuator transmission. All of them are optional, and exactly one of them must be specified. If this attribute is specified, the actuator acts on the given joint.

For **hinge** and **slide** joints, the actuator length equals the joint position/angle times the first element of <span class="at">gear</span>.

For **ball** joints, the first three elements of gear define a 3d rotation axis in the child frame around which the actuator produces torque. The actuator length is defined as the dot-product between this gear axis and the angle-axis representation of the joint quaternion, and is in units of radian if <span class="at">gear</span> is normalized (generally scaled by the norm of <span class="at">gear</span>). Note that the length is defined on a circle: after total rotation of more than $`\pi`$ it wraps to $`-\pi`$, and vice-versa. [position](XMLreference.md) and [intvelocity](XMLreference.md) servos on such transmissions interpret their setpoint on the circle, driving towards the nearest representative of the target, so targets can be wound continuously through any number of turns and no control limits are required to prevent wrapping.

For **free** joints, gear defines a 3d translation axis in the world frame followed by a 3d rotation axis in the child frame. The actuator generates force and torque relative to the specified axes. The actuator length for free joints is defined as zero (so cannot be used with position servos).



<span class="at">jointinparent</span>: <span class="at-val">string, optional</span>  
Identical to joint, except that for ball and free joints, the 3d rotation axis given by gear is defined in the parent frame (which is the world frame for free joints) rather than the child frame.



<span class="at">site</span>: <span class="at-val">string, optional</span>  
This transmission can apply force and torque at a site. The gear vector defines a 3d translation axis followed by a 3d rotation axis. Both are defined in the site's frame. This can be used to model jets and propellers. The effect is similar to actuating a free joint, and the actuator length is defined as zero unless a <span class="at">refsite</span> is defined (see below). One difference from the <span class="at">joint</span> and <span class="at">jointinparent</span> transmissions above is that here the actuator operates on a site rather than a joint, but this difference disappears when the site is defined at the frame origin of the free-floating body. The other difference is that for site transmissions both the translation and rotation axes are defined in local coordinates. In contrast, translation is global and rotation is local for <span class="at">joint</span>, and both translation and rotation are global for <span class="at">jointinparent</span>.



s-0JHanqV1A



<span class="at">refsite</span>: <span class="at-val">string, optional</span>  
When using a <span class="at">site</span> transmission, measure the translation and rotation w.r.t the frame of the <span class="at">refsite</span>. In this case the actuator *does* have length and <span class="el">position</span> actuators can be used to directly control an end effector, see [refsite.xml](https://github.com/google-deepmind/mujoco/tree/main/test/engine/testdata/actuation/refsite.xml) example model. As above, the length is the dot product of the <span class="at">gear</span> vector and the frame difference. So `gear="0 1 0 0 0 0"` means "Y-offset of <span class="at">site</span> in the <span class="at">refsite</span> frame", while `gear="0 0 0 0 0 1"` means rotation "Z- rotation of <span class="at">site</span> in the <span class="at">refsite</span> frame". It is recommended to use a normalized <span class="at">gear</span> vector with nonzeros in only the first 3 *or* the last 3 elements of <span class="at">gear</span>, so the actuator length will be in either length units or radians, respectively. As with ball joints (see [general/joint](XMLreference.md) above), rotational lengths are defined on a circle and servo setpoints are interpreted on it; control limits are not required to prevent wrapping.



<span class="at">body</span>: <span class="at-val">string, optional</span>  
This transmission can apply linear forces at contact points in the direction of the contact normal. The set of contacts is all those belonging to the specified <span class="at">body</span>. This can be used to model natural active adhesion mechanisms like the feet of geckos and insects. The actuator length is again defined as zero. For more information, see the [adhesion](XMLreference.md) shortcut below.



<span class="at">tendon</span>: <span class="at-val">string, optional</span>  
If specified, the actuator acts on the given tendon. The actuator length equals the tendon length times the gear ratio. Both spatial and fixed tendons can be used.



<span class="at">cranksite</span>: <span class="at-val">string, optional</span>  
If specified, the actuator acts on a slider-crank mechanism which is implicitly determined by the actuator (i.e., it is not a separate model element). The specified site corresponds to the pin joining the crank and the connecting rod. The actuator length equals the position of the slider-crank mechanism times the gear ratio.



<span class="at">slidersite</span>: <span class="at-val">string, required for slider-crank transmission</span>  
Used only for the slider-crank transmission type. The specified site is the pin joining the slider and the connecting rod. The slider moves along the z-axis of the slidersite frame. Therefore the site should be oriented as needed when it is defined in the kinematic tree; its orientation cannot be changed in the actuator definition.



<span class="at">user</span>: <span class="at-val">real(nuser_actuator), "0 ... 0"</span>  
See [User parameters](modeling.md).



<span class="at">actdim</span>: <span class="at-val">real, "-1"</span>  
Dimension of the activation state. The default value of `-1` instructs the compiler to set the dimension according to the <span class="at">dyntype</span>. Values larger than `1` are only allowed for user-defined activation dynamics, as native types require dimensions of only 0 or 1. For activation dimensions bigger than 1, the *last element* is used to generate force.



<span class="at">dyntype</span>: <span class="at-val">\[none, integrator, filter, filterexact, pid, dcmotor, muscle, user\], "none"</span>  
Activation dynamics type for the actuator. The available dynamics types were already described in the [Actuation model](computation/index.md) section. Repeating that description in somewhat different notation (corresponding to the mjModel and mjData fields involved) we have:

| Keyword     | Description                                                  |
|-------------|--------------------------------------------------------------|
| none        | No internal state                                            |
| integrator  | act_dot = ctrl                                               |
| filter      | act_dot = (ctrl - act) / dynprm\[0\]                         |
| filterexact | Like filter but with exact integration                       |
| pid         | act_dot = position error; see [pid](XMLreference.md)         |
| dcmotor     | DC motor electrical dynamics, see [dcmotor](XMLreference.md) |
| muscle      | act_dot = mju_muscleDynamics(...)                            |
| user        | act_dot = mjcb_act_dyn(...)                                  |



<span class="at">gaintype</span>: <span class="at-val">\[fixed, affine, muscle, dcmotor, pid, so3, user\], "fixed"</span>  
The gain and bias together determine the output of the force generation mechanism, which is currently assumed to be affine. As already explained in [Actuation model](computation/index.md), the general formula is: scalar_force = gain_term \* (act or ctrl) + bias_term. The formula uses the activation state when present, and the control otherwise. The keywords have the following meaning:

| Keyword | Description |
|----|----|
| fixed | gain_term = gainprm\[0\] |
| affine | gain_term = gain_prm\[0\] + gain_prm\[1\]\*length + gain_prm\[2\]\*velocity |
| muscle | gain_term = mju_muscleGain(...) |
| dcmotor | DC motor gain (K or K/R), see [dcmotor](XMLreference.md) |
| pid | PID controller with setpoint inputs, see [pid](XMLreference.md) |
| so3 | geodesic orientation servo, computed jointly over 3 force outputs, see [orientation](XMLreference.md) |
| user | gain_term = mjcb_act_gain(...) |



<span class="at">biastype</span>: <span class="at-val">\[none, affine, muscle, dcmotor, so3, user\], "none"</span>  
The keywords have the following meaning:

| Keyword | Description |
|----|----|
| none | bias_term = 0 |
| affine | bias_term = biasprm\[0\] + biasprm\[1\]\*length + biasprm\[2\]\*velocity |
| muscle | bias_term = mju_muscleBias(...) |
| dcmotor | DC motor bias: back-EMF, cogging, LuGre friction, see [dcmotor](XMLreference.md) |
| so3 | damping term of the geodesic orientation servo, see [orientation](XMLreference.md) |
| user | bias_term = mjcb_act_bias(...) |

Note that <span class="at">gaintype</span> and <span class="at">biastype</span> must either both be "so3" or neither.



<span class="at">dynprm</span>: <span class="at-val">real(10), "1 0 ... 0"</span>  
Activation dynamics parameters. The built-in activation types (except for muscle) use only the first parameter, but we provide additional parameters in case user callbacks implement a more elaborate model. The length of this array is not enforced by the parser, so the user can enter as many parameters as needed. These defaults are not compatible with muscle actuators; see [muscle](XMLreference.md) below.



<span class="at">gainprm</span>: <span class="at-val">real(10), "1 0 ... 0"</span>  
Gain parameters. The built-in gain types (except for muscle) use only the first parameter, but we provide additional parameters in case user callbacks implement a more elaborate model. The length of this array is not enforced by the parser, so the user can enter as many parameters as needed. These defaults are not compatible with muscle actuators; see [muscle](XMLreference.md) below.



<span class="at">biasprm</span>: <span class="at-val">real(10), "0 ... 0"</span>  
Bias parameters. The affine bias type uses three parameters. The length of this array is not enforced by the parser, so the user can enter as many parameters as needed. These defaults are not compatible with muscle actuators; see [muscle](XMLreference.md) below.



<span class="at">velrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range of the velocity-setpoint input of a [pid](XMLreference.md) actuator.



<span class="at">ffrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range of the feedforward input of a [pid](XMLreference.md) actuator.



<span class="at">inheritrange</span>: <span class="at-val">real, "0"</span>  
Sets the range of a position servo from the range of its joint or tendon, as described in [position/inheritrange](XMLreference.md): the <span class="at">ctrlrange</span>, or the <span class="at">actrange</span> if <span class="at">dyntype</span> is "integrator". It has an effect on an actuator with affine bias and either fixed gain, where `gainprm[0]` equals `-biasprm[1]`, or gaintype "pid": the actuators which the [position](XMLreference.md), [intvelocity](XMLreference.md) and [pid](XMLreference.md) shortcuts create.



<span class="at">input</span>: <span class="at-val">string, optional</span>  
Input signature of the actuator: which controls make up its control block, recorded in `mjModel.actuator_ctrlspec`. For gaintype "so3" it selects the orientation chart: "expmap" (3 controls, the default) or "quat" (4 controls); see [orientation/input](XMLreference.md). For gaintypes "pid" and "dcmotor" it is a token list selecting the input subset; see [pid/input](XMLreference.md) and [dcmotor/input](XMLreference.md). For gaintypes "fixed" and "affine" it declares what the single control is, and does not affect the simulation: "pos", a position setpoint; "vel", a velocity setpoint; "pressure", a pressure, the gain being an area. Without a declaration the control is a command, scaled by the gain. The [position](XMLreference.md), [velocity](XMLreference.md), [intvelocity](XMLreference.md) and [cylinder](XMLreference.md) shortcuts declare "pos", "vel", "vel" and "pressure" respectively, and *mj_actuatorInputName* returns the declaration. An input signature inherited from a default class is discarded when the gaintype changes; `input=""` restores the gaintype's default.



<span class="at">actearly</span>: <span class="at-val">\[false, true\], "false"</span>  
If true, force computation will use the next value of the activation variable rather than the current one. Setting this flag reduces the delay between the control and accelerations by one time-step.


#### <span class="el-prefix">actuator/</span> ⁠ **motor** ​

This and the next three elements are the [Actuator shortcuts](modeling.md) discussed earlier. When such a shortcut is encountered, the parser creates a <span class="el">general</span> actuator and sets its dynprm, gainprm and biasprm attributes to the internal defaults shown above, regardless of any default settings. It then adjusts dyntype, gaintype and biastype depending on the shortcut, parses any custom attributes (beyond the common ones), and translates them into regular attributes (i.e., attributes of the <span class="el">general</span> actuator type) as explained here.

This element creates a direct-drive actuator. The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting | Attribute | Setting |
|-----------|---------|-----------|---------|
| dyntype   | none    | dynprm    | 1 0 0   |
| gaintype  | fixed   | gainprm   | 1 0 0   |
| biastype  | none    | biasprm   | 0 0 0   |

This element does not have custom attributes. It only has common attributes, which are:















































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">site</span>, <span class="at">refsite</span>, <span class="at">user</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).

#### <span class="el-prefix">actuator/</span> ⁠ **position** ​

This element creates a position servo with an optional first-order filter. The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting             | Attribute | Setting       |
|-----------|---------------------|-----------|---------------|
| dyntype   | none or filterexact | dynprm    | timeconst 0 0 |
| gaintype  | fixed               | gainprm   | kp 0 0        |
| biastype  | affine              | biasprm   | 0 -kp -kv     |
| input     | pos                 |           |               |

On purely rotational transmissions, setpoints are interpreted on the circle; see [gear](XMLreference.md).

This element has one custom attribute in addition to the common attributes:















































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">site</span>, <span class="at">refsite</span>, <span class="at">user</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">kp</span>: <span class="at-val">real, "1"</span>  
Position feedback gain.



<span class="at">kv</span>: <span class="at-val">real, "0"</span>  
Damping applied by the actuator. When using this attribute, it is recommended to use the implicitfast or implicit [integrators](computation/index.md).



<span class="at">dampratio</span>: <span class="at-val">real, "0"</span>  
Damping applied by the actuator, using damping ratio units. This attribute is exclusive with <span class="at">kv</span> and has similar meaning, but instead of units of force/velocity, the units are $`2 \sqrt{k_p \cdot m}`$, corresponding to a harmonic oscillator's [damping ratio](https://en.wikipedia.org/wiki/Damping#Damping_ratio_definition). A value of 1 corresponds to a *critically damped* oscillator, which often produces desirable behavior. Values smaller or larger than 1 correspond to underdamped and overdamped oscillations, respectively. The reflected mass $`m = (J M^{-1} J^T)^{-1}`$ is computed at the reference configuration `mjModel.qpos0` from the actuator transmission Jacobian $`J`$ and inertia matrix $`M`$ (averaged across force outputs for multi-output actuators), taking into account joint [armature](XMLreference.md), tendon [armature](XMLreference.md), and actuator [armature](XMLreference.md). However, passive [damping](XMLreference.md) or [frictionloss](XMLreference.md) in the affected joints or tendons are not taken into account; if they are non-negligible, <span class="at">dampratio</span> values smaller than 1 might be required to achieve desirable motion. When using this attribute, it is recommended to use the implicitfast or implicit [integrators](computation/index.md).



<span class="at">timeconst</span>: <span class="at-val">real, "0"</span>  
Time-constant of optional first-order filter. If larger than zero, the actuator uses the <span class="at">filterexact</span> [dynamics type](XMLreference.md), if zero (the default) no filter is used.



<span class="at">inheritrange</span>: <span class="at-val">real, "0"</span>  
Automatically set the actuator's <span class="at">ctrlrange</span> to match the transmission target's <span class="at">range</span>. The default value means "disabled". A positive value <span class="at-val">X</span> sets the <span class="at">ctrlrange</span> around the midpoint of the target range, scaled by <span class="at-val">X</span>. For example if the target joint has <span class="at">range</span> of <span class="at-val">\[0, 1\]</span>, then a value of <span class="at-val">1.0</span> will set <span class="at">ctrlrange</span> to <span class="at-val">\[0, 1\]</span>; values of <span class="at-val">0.8</span> and <span class="at-val">1.2</span> will set the <span class="at">ctrlrange</span> to <span class="at-val">\[0.1, 0.9\]</span> and <span class="at-val">\[-0.1, 1.1\]</span>, respectively. Values smaller than 1 are useful for not hitting the limits; values larger than 1 are useful for maintaining control authority at the limits (being able to push on them). This attribute is exclusive with <span class="at">ctrlrange</span> and available only for joint and tendon transmissions which have <span class="at">range</span> defined. A model which is saved [as it was compiled](XMLreference.md) has the explicit <span class="at">ctrlrange</span> at the actuator in place of this attribute.


#### <span class="el-prefix">actuator/</span> ⁠ **pid** ​

This element creates a PID controller with position and velocity setpoint inputs on a single force output, with optional integral action and feedforward. With the default input signature `[pos, vel]` the force is $`k_p (u_{pos} - l) + k_v (u_{vel} - v)`$ where $`l, v`$ are the actuator length and velocity; with a zero velocity setpoint this is identical to [position](XMLreference.md). The input signature is any subset of `[pos, vel, ff]`, selected by [input](XMLreference.md): an absent setpoint input is fixed at zero, and the `ff` input adds a feedforward force. Integral action is enabled by [ki](XMLreference.md): the position error is integrated in [act](programming/simulation.md) and contributes $`k_i \cdot act`$ to the force, with anti-windup clamping by [imax](XMLreference.md). [slewmax](XMLreference.md) limits the rate of change of the effective position setpoint. Each of these features, when enabled, adds one activation state, in the order \[slew, integral\]. The underlying [general](XMLreference.md) attributes are set as follows:

| Attribute | Setting            | Attribute | Setting   |
|-----------|--------------------|-----------|-----------|
| dyntype   | none or pid dynprm | imax 0 0  |           |
| gaintype  | pid                | gainprm   | ki 0 0    |
| biastype  | affine             | biasprm   | 0 -kp -kv |

This element has custom attributes in addition to the common attributes:

























<span class="at">kp</span>: <span class="at-val">real, "1"</span>  
Position feedback gain.


























<span class="at">kv</span>: <span class="at-val">real, "0"</span>  
Velocity feedback gain: applied to the velocity error when the `vel` input is present, and as pure damping otherwise. When using this attribute, it is recommended to use the implicitfast or implicit [integrators](computation/index.md).



<span class="at">dampratio</span>: <span class="at-val">real, "0"</span>  
Damping applied by the actuator, using damping ratio units, as for [position/dampratio](XMLreference.md). This attribute is exclusive with <span class="at">kv</span>.



<span class="at">ki</span>: <span class="at-val">real, "0"</span>  
Integral gain. A nonzero value enables integral action: the position error is integrated in [act](programming/simulation.md) ([dyntype](XMLreference.md) "pid") and contributes $`k_i \cdot act`$ to the force. Requires the `pos` input.



<span class="at">imax</span>: <span class="at-val">real, "0"</span>  
Anti-windup limit on the integral state: accumulation stops beyond ±<span class="at">imax</span>. The default value 0 means "unclamped".



<span class="at">slewmax</span>: <span class="at-val">real, "0"</span>  
Maximum rate of change of the effective position setpoint. When positive, the commanded setpoint is rate-limited through an activation state holding the effective setpoint, as for the [dcmotor controller](XMLreference.md). The default value 0 means "unlimited".



<span class="at">input</span>: <span class="at-val">string, "pos vel"</span>  
Input signature: a space-separated subset of the tokens "pos", "vel" and "ff", packed in this canonical order. Absent setpoint inputs are fixed at zero, so the control vector contains no inert entries.



<span class="at">posrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range of the position-setpoint input; an alias of [ctrlrange](XMLreference.md) (the first input).



<span class="at">velrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range of the velocity-setpoint input.



<span class="at">ffrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range of the feedforward input.



<span class="at">inheritrange</span>: <span class="at-val">real, "0"</span>  
Identical to [position/inheritrange](XMLreference.md), setting <span class="at">posrange</span> from the transmission target's <span class="at">range</span>.


#### <span class="el-prefix">actuator/</span> ⁠ **orientation** ​


17XpwnqyCXs


This element creates an orientation servo: a geodesic PD controller on a relative orientation, targeting a ball [joint](XMLreference.md) or a [site](XMLreference.md) with a [refsite](XMLreference.md). Unlike per-axis [position](XMLreference.md) servos, the servo acts jointly on the full orientation: the force is $`k_p \log(q^{-1} q_{target}) - k_v \omega`$, exact for arbitrary axis combinations, with a unique equilibrium at every commanded orientation. The transmission has 3 force outputs; force, error and angular velocity are expressed in the child (joint or site) frame. The commanded orientation is given in the [input](XMLreference.md) chart: an exponential-map vector (3 controls, the default) or a quaternion (4 controls). [forcerange](XMLreference.md) clamps the norm of the output torque, preserving its direction; the lower bound must be 0. [Actuator sensors](XMLreference.md) report one value per force output. The integrator variant, which stores the orientation setpoint in [act](programming/simulation.md), is available via [general](XMLreference.md) with [dyntype](XMLreference.md) "integrator" and is expmap-only. The video on the right shows this [example model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/actuation/orientation.xml). The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting | Attribute | Setting   |
|-----------|---------|-----------|-----------|
| dyntype   | none    | gainprm   | kp 0 0    |
| gaintype  | so3     | biasprm   | 0 -kp -kv |
| biastype  | so3     |           |           |


<span class="at">ctrlrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping the control input, as described in [ctrlrange](XMLreference.md). For this multi-input actuator, the same range limits are replicated and applied independently to each of the 3 (expmap) or 4 (quaternion) control inputs in the control block.



<span class="at">forcerange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping the torque output, as described in [forcerange](XMLreference.md). The torque is clamped on its norm, preserving its direction: the second value bounds the torque magnitude and the first value must be 0.


This element has custom attributes in addition to the common attributes:













<span class="at">kp</span>: <span class="at-val">real, "1"</span>  
Position feedback gain, in units of torque per radian of geodesic error.














<span class="at">kv</span>: <span class="at-val">real, "0"</span>  
Damping applied by the actuator, per force output. When using this attribute, it is recommended to use the implicitfast or implicit [integrators](computation/index.md).



<span class="at">dampratio</span>: <span class="at-val">real, "0"</span>  
Damping applied by the actuator, using damping ratio units, as for [position/dampratio](XMLreference.md). This attribute is exclusive with <span class="at">kv</span>.



<span class="at">input</span>: <span class="at-val">\[expmap, quat\], "expmap"</span>  
[Chart](https://en.wikipedia.org/wiki/Manifold#Charts) of the commanded orientation. With "expmap" the control block is an exponential-map vector (3 controls, in radians). With "quat" the control block is a quaternion (4 controls, [w-first](programming/simulation.md)); the commanded quaternion is normalized by the servo, making the force scale- and antipodally-invariant, and the control block resets to the identity quaternion. The quat chart requires `dyntype="none"`.


#### <span class="el-prefix">actuator/</span> ⁠ **velocity** ​

This element creates a velocity servo. Note that a PD controller with both position and velocity setpoint inputs is provided by the [pid](XMLreference.md) actuator. When using this actuator, it is recommended to use the implicitfast or implicit [integrators](computation/index.md). The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting | Attribute | Setting |
|-----------|---------|-----------|---------|
| dyntype   | none    | dynprm    | 1 0 0   |
| gaintype  | fixed   | gainprm   | kv 0 0  |
| biastype  | affine  | biasprm   | 0 0 -kv |
| input     | vel     |           |         |

This element has one custom attribute in addition to the common attributes:















































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">site</span>, <span class="at">refsite</span>, <span class="at">user</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">kv</span>: <span class="at-val">real, "1"</span>  
Velocity feedback gain.


#### <span class="el-prefix">actuator/</span> ⁠ **intvelocity** ​

This element creates an integrated-velocity servo. For more information, see the [Activation clamping](modeling.md) section of the Modeling chapter. The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting    | Attribute | Setting   |
|-----------|------------|-----------|-----------|
| dyntype   | integrator | dynprm    | 1 0 0     |
| gaintype  | fixed      | gainprm   | kp 0 0    |
| biastype  | affine     | biasprm   | 0 -kp -kv |
| input     | vel        |           |           |

Activation clamping is controlled by <span class="at">actlimited</span> and <span class="at">actrange</span>, like any stateful actuator. On purely rotational transmissions, setpoints are interpreted on the circle, as for [position](XMLreference.md); the integrated setpoint is re-anchored to a bounded representative at each timestep, so clamping is not required for winding targets.

This element has one custom attribute in addition to the common attributes:



















































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">actlimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">actrange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">site</span>, <span class="at">refsite</span>, <span class="at">user</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">kp</span>: <span class="at-val">real, "1"</span>  
Position feedback gain.



<span class="at">kv</span>: <span class="at-val">real, "0"</span>  
Damping applied by the actuator. When using this attribute, it is recommended to use the implicitfast or implicit [integrators](computation/index.md).



<span class="at">dampratio</span>: <span class="at-val">real, "0"</span>  
See [position/dampratio](XMLreference.md).



<span class="at">inheritrange</span>: <span class="at-val">real, "0"</span>  
Identical to [position/inheritrange](XMLreference.md), but sets <span class="at">actrange</span> (which has the same length semantics as the transmission target) rather than <span class="at">ctrlrange</span> (which has velocity semantics).


#### <span class="el-prefix">actuator/</span> ⁠ **damper** ​

This element is an active damper which produces a force proportional to both velocity and control: `F = - kv * velocity * control`, where `kv` must be nonnegative. <span class="at">ctrlrange</span> is required and must also be nonnegative. When using this actuator, it is recommended to use the implicitfast or implicit [integrators](computation/index.md). The underlying <span class="el">general</span> attributes are set as follows:

| Attribute   | Setting | Attribute | Setting |
|-------------|---------|-----------|---------|
| dyntype     | none    | dynprm    | 1 0 0   |
| gaintype    | affine  | gainprm   | 0 0 -kv |
| biastype    | none    | biasprm   | 0 0 0   |
| ctrllimited | true    |           |         |

This element has one custom attribute in addition to the common attributes:















































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">site</span>, <span class="at">refsite</span>, <span class="at">user</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">kv</span>: <span class="at-val">real, "1"</span>  
Velocity feedback gain.


#### <span class="el-prefix">actuator/</span> ⁠ **cylinder** ​

This element is suitable for modeling pneumatic or hydraulic cylinders. The control is the commanded pressure; the activation is the pressure in the cylinder, which follows the control with time constant <span class="at">timeconst</span>, and the force is the pressure times <span class="at">area</span>, plus the bias. The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting  | Attribute | Setting       |
|-----------|----------|-----------|---------------|
| dyntype   | filter   | dynprm    | timeconst 0 0 |
| gaintype  | fixed    | gainprm   | area 0 0      |
| biastype  | affine   | biasprm   | bias(3)       |
| input     | pressure |           |               |

This element has four custom attributes in addition to the common attributes:















































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">site</span>, <span class="at">refsite</span>, <span class="at">user</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">timeconst</span>: <span class="at-val">real, "1"</span>  
Time constant of the activation dynamics.



<span class="at">area</span>: <span class="at-val">real, "1"</span>  
Area of the cylinder. This is used internally as actuator gain.



<span class="at">diameter</span>: <span class="at-val">real, optional</span>  
Instead of area the user can specify diameter. If both are specified, diameter has precedence.



<span class="at">bias</span>: <span class="at-val">real(3), "0 0 0"</span>  
Bias parameters, copied internally into biasprm.


#### <span class="el-prefix">actuator/</span> ⁠ **muscle** ​

This element is used to model a muscle actuator, as described in the [Muscles actuators](modeling.md) section. The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting | Attribute | Setting |
|----|----|----|----|
| dyntype | muscle | dynprm | timeconst(2) tausmooth |
| gaintype | muscle | gainprm | range(2), force, scale, lmin, lmax, vmax, fpmax, fvmax |
| biastype | muscle | biasprm | same as gainprm |

This element has nine custom attributes in addition to the common attributes:











































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">user</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">timeconst</span>: <span class="at-val">real(2), "0.01 0.04"</span>  
Time constants for activation and de-activation dynamics.



<span class="at">tausmooth</span>: <span class="at-val">real, "0"</span>  
Width of smooth transition between activation and deactivation time constants. Units of ctrl, must be nonnegative.



<span class="at">range</span>: <span class="at-val">real(2), "0.75 1.05"</span>  
Operating length range of the muscle, in units of L0.



<span class="at">force</span>: <span class="at-val">real, "-1"</span>  
Peak active force at rest. If this value is negative, the peak force is determined automatically using the scale attribute below.



<span class="at">scale</span>: <span class="at-val">real, "200"</span>  
If the force attribute is negative, the peak active force for the muscle is set to this value divided by mjModel.actuator_acc0. The latter is the norm of the joint-space acceleration vector caused by unit force on the actuator's transmission in qpos0. In other words, scaling produces higher peak forces for muscles that pull more weight.



<span class="at">lmin</span>: <span class="at-val">real, "0.5"</span>  
Lower position range of the normalized FLV curve, in units of L0.



<span class="at">lmax</span>: <span class="at-val">real, "1.6"</span>  
Upper position range of the normalized FLV curve, in units of L0.



<span class="at">vmax</span>: <span class="at-val">real, "1.5"</span>  
Shortening velocity at which muscle force drops to zero, in units of L0 per second.



<span class="at">fpmax</span>: <span class="at-val">real, "1.3"</span>  
Passive force generated at lmax, relative to the peak rest force.



<span class="at">fvmax</span>: <span class="at-val">real, "1.2"</span>  
Active force generated at saturating lengthening velocity, relative to the peak rest force.


#### <span class="el-prefix">actuator/</span> ⁠ **adhesion** ​


BcHZ5BFeTmU


This element defines an active adhesion actuator which injects forces at contacts in the normal direction, see illustration video. The model shown in the video can be found [here](https://github.com/google-deepmind/mujoco/tree/main/model/adhesion) and includes inline annotations. The transmission target is a <span class="el">body</span>, and adhesive forces are injected into all contacts involving geoms which belong to this body. The force is divided equally between multiple contacts. When the [gap](XMLreference.md) attribute is not used, this actuator requires active contacts and cannot apply a force at a distance, more like the active adhesion on the feet of geckos and insects rather than an industrial vacuum gripper. In order to enable "suction at a distance", set the [gap](XMLreference.md) attribute of the body's geoms to a positive value. This creates a layer around each geom where contacts are detected but no contact forces are generated, and the adhesive force can act across this gap. In the video above, such inactive contacts are blue, while active contacts are orange. An adhesion actuator's length is always 0. <span class="at">ctrlrange</span> is required and must also be nonnegative (no repulsive forces are allowed). For adhesion as a *passive* property of the contacting surfaces — always on, per contact, and leaving resting penetration unaffected — see the [geom/adhesion](XMLreference.md) attribute. The underlying <span class="el">general</span> attributes are set as follows:

| Attribute | Setting | Attribute   | Setting  |
|-----------|---------|-------------|----------|
| dyntype   | none    | dynprm      | 1 0 0    |
| gaintype  | fixed   | gainprm     | gain 0 0 |
| biastype  | none    | biasprm     | 0 0 0    |
| trntype   | body    | ctrllimited | true     |

This element has a subset of the common attributes and two custom attributes.





















<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">user</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">body</span>: <span class="at-val">string, required</span>  
The actuator acts on all contacts involving this body's geoms.



<span class="at">gain</span>: <span class="at-val">real, "1"</span>  
Gain of the adhesion actuator, in units of force. The total adhesion force applied by the actuator is the control value multiplied by the gain. This force is distributed equally between all the contacts involving geoms belonging to the target body.


#### <span class="el-prefix">actuator/</span> ⁠ **dcmotor** ​

This element creates a DC motor actuator. See the [DC motor technical note](_static/dcmotor.pdf) for complete mathematical formulations and parameter semantics, but we include a few important notes below. Note that <span class="el">dcmotor</span> does not conform to the affine gain / bias structure of the [general actuation model](computation/index.md), except for the stateless case.

- [resistance](XMLreference.md), [motorconst](XMLreference.md) and [nominal](XMLreference.md) are each optional, but some combination of them is required. See Section 2.1 of the [technical note](_static/dcmotor.pdf).
- The control block is selected by [input](XMLreference.md): any subset of `[pos, vel, ff]`, where `pos` and `vel` are setpoint inputs to the on-board [PID controller](XMLreference.md) and `ff` is a torque feedforward added to its output; the `voltage` input is the raw terminal voltage. The default is the plain voltage-commanded motor. With `input="none"` the actuator has no control inputs at all and acts as a purely passive device.
- Optional features include electrical dynamics ([inductance](XMLreference.md)), [cogging torque](XMLreference.md), [thermal resistance variation](XMLreference.md), and [LuGre](XMLreference.md) friction.

The underlying <span class="el">general</span> attributes are set to the <span class="el">dcmotor</span> type, and their associated parameter arrays are computed internally:

| Attribute | Setting | Attribute | Setting  |
|-----------|---------|-----------|----------|
| dyntype   | dcmotor | dynprm    | computed |
| gaintype  | dcmotor | gainprm   | computed |
| biastype  | dcmotor | biasprm   | computed |

This element has the following custom attributes in addition to the common attributes:











































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">nsample</span>, <span class="at">interp</span>, <span class="at">delay</span>, <span class="at">ctrllimited</span>, <span class="at">ctrlrange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">damping</span>, <span class="at">armature</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">site</span>, <span class="at">refsite</span>, <span class="at">user</span>  
Same as in actuator/ [general](XMLreference.md).


<span class="at">resistance</span>: <span class="at-val">real, optional</span>  
Terminal resistance $`R`$ in Ohm. (see [tech note](_static/dcmotor.pdf), Sections 1.1 and 2.1)



<span class="at">motorconst</span>: <span class="at-val">real(2), optional</span>  
Motor constants, defined as <span class="at">motorconst</span> = "<span class="at-val">Kt</span> <span class="at-val">Ke</span>" (N·m/A, equivalently V·s/rad). <span class="at-val">Kt</span> is the torque constant and <span class="at-val">Ke</span> the back-EMF constant; they can differ when magnetic saturation is present. If both are positive, the effective constant is $`K = \sqrt{K_t K_e}`$ (geometric mean). If only one is positive, $`K`$ equals that value. If a datasheet specifies the speed constant $`K_v`$ in rad/(V·s), use $`K_e = 1/K_v`$. Both constants must be non-negative, and $`K`$ must be positive unless [input](XMLreference.md) is "none". (see [tech note](_static/dcmotor.pdf), Sections 1.1 and 2.1)



<span class="at">nominal</span>: <span class="at-val">real(3), optional</span>  
Nominal operating point, defined as <span class="at">nominal</span> = "<span class="at-val">voltage</span> <span class="at-val">stall_torque</span> <span class="at-val">no_load_speed</span>". The compiler derives $`K =`$ <span class="at-val">voltage</span> / <span class="at-val">no_load_speed</span> and $`R =
K`$ · <span class="at-val">voltage</span> / <span class="at-val">stall_torque</span>. (see [tech note](_static/dcmotor.pdf), Sections 1.1 and 2.1)



<span class="at">inductance</span>: <span class="at-val">real(2), "0 0"</span>  
Electrical dynamics, defined as <span class="at">inductance</span> = "<span class="at-val">L</span> <span class="at-val">timeconst</span>" (Henry, seconds). These are alternative specifications: <span class="at-val">L</span> is the winding inductance and <span class="at-val">timeconst</span> $`= L/R`$ is the electrical time constant. Specify one; if both are given, <span class="at-val">L</span> takes precedence. If both are 0 (the default), no electrical dynamics are modeled and the current is computed algebraically. Adds one activation variable for armature current. (see [tech note](_static/dcmotor.pdf), Sections 1.1.1 and 2.2)



<span class="at">thermal</span>: <span class="at-val">real(6), "0 0 0 0 0 0"</span>  
Thermal model, defined as <span class="at">thermal</span> = "<span class="at-val">resistance</span> <span class="at-val">capacitance</span> <span class="at-val">timeconst</span> <span class="at-val">tempcoef</span> <span class="at-val">reftemp</span> <span class="at-val">ambient</span>" (K/W, J/K, s, 1/K, °C, °C). The first three sub-values specify the thermal time constant: <span class="at-val">timeconst</span> = <span class="at-val">resistance</span> $`\times`$ <span class="at-val">capacitance</span>. Specify any two of them; if all three are given, <span class="at-val">capacitance</span> = <span class="at-val">timeconst</span> / <span class="at-val">resistance</span>. If all are 0 (the default), thermal modeling is disabled. Adds one activation variable for winding temperature. (see [tech note](_static/dcmotor.pdf), Sections 1.3 and 2.3)



<span class="at">saturation</span>: <span class="at-val">real(3), "0 0 0"</span>  
Limits on the actuator, defined as <span class="at">saturation</span> = "<span class="at-val">torque</span> <span class="at-val">current</span> <span class="at-val">current_rate</span>". <span class="at-val">torque</span> and <span class="at-val">current</span> are alternative specifications of the maximum continuous torque: if <span class="at-val">current</span> is given, <span class="at-val">torque</span> $`= K \cdot`$ <span class="at-val">current</span>; if both are given, <span class="at-val">torque</span> takes precedence. Sets <span class="at">forcerange</span> to \[$`-\tau_{\max},\, \tau_{\max}`$\]. An authored <span class="at">saturation</span> clears any inherited <span class="at">forcerange</span> before applying these limits. <span class="at-val">current_rate</span> sets the maximum rate of change of current $`(di/dt)_{\max}`$ (requires [inductance](XMLreference.md)). A value of 0 (the default) for any sub-value disables the respective limit. (see [tech note](_static/dcmotor.pdf), Section 2)



<span class="at">cogging</span>: <span class="at-val">real(3), "0 0 0"</span>  
Cogging torque, defined as <span class="at">cogging</span> = "<span class="at-val">amplitude</span> <span class="at-val">poles</span> <span class="at-val">phase</span>" (N·m, integer, rad). Adds a position-dependent torque $`= \textsf{amplitude} \cdot \sin(\textsf{poles} \cdot \theta +
\textsf{phase})`$. Disabled when <span class="at-val">amplitude</span> = 0 (the default). (see [tech note](_static/dcmotor.pdf), Sections 1.2 and 2.1)



<span class="at">lugre</span>: <span class="at-val">real(5), "0 0 0 0 0"</span>  
LuGre friction, defined as <span class="at">lugre</span> = "<span class="at-val">stiffness</span> <span class="at-val">damping</span> <span class="at-val">coulomb</span> <span class="at-val">static</span> <span class="at-val">stribeck</span>" (N·m/rad, N·m·s/rad, N·m, N·m, rad/s). Disabled when <span class="at-val">stiffness</span> = 0 (the default). Adds one activation variable for bristle deflection. Note that the viscous damping coefficient $`\sigma_2`$ is not part of the <span class="at">lugre</span> attribute and should be added to the standard actuator [damping](XMLreference.md) attribute. (see [tech note](_static/dcmotor.pdf), Sections 1.4 and 2.4)



<span class="at">input</span>: <span class="at-val">string, "voltage"</span>  
Input signature: a space-separated subset of the tokens "pos", "vel", "ff" and "voltage", required in this canonical order. The `pos` and `vel` inputs are setpoints for the on-board [controller](XMLreference.md), and `ff` is a torque feedforward added to its output, as for [pid/input](XMLreference.md). The `voltage` input is different in kind: it is the raw terminal voltage of the physical device, applied downstream of the controller and its <span class="at-val">Vmax</span> clamp. `input="voltage"` (the default) is the plain voltage-commanded motor. Absent setpoint inputs are fixed at zero. The keyword "none" selects the empty signature: the actuator has no control inputs and is purely passive, useful for modeling [friction](XMLreference.md) and [cogging](XMLreference.md) as passive joint forces. The terminal voltage is zero, so back-EMF drives current through the (shorted) motor and brakes the joint; setting [motorconst](XMLreference.md) to zero disables the electrical branch ([resistance](XMLreference.md) must still be positive). (see [tech note](_static/dcmotor.pdf), Section 2.5)



<span class="at">controller</span>: <span class="at-val">real(6), "0 0 0 0 0 0"</span>  
PID controller parameters, defined as <span class="at">controller</span> = "<span class="at-val">kp</span> <span class="at-val">ki</span> <span class="at-val">kd</span> <span class="at-val">slewmax</span> <span class="at-val">Imax</span> <span class="at-val">Vmax</span>". The gains are in torque space, as for [pid](XMLreference.md): the controller commands the torque $`\tau = k_p (u_{pos} - l) + k_d (u_{vel} - \dot{l}) + k_i x_I + u_{f\!f}`$ over the inputs present in the [input](XMLreference.md) signature, absent setpoints being fixed at zero, and drives the voltage $`v = (R/K)\,\tau + K \dot{l}`$, the second term compensating back-EMF as in a current-controlled driver: commanded torque is delivered exactly until a limit is reached. Torque-space gains from datasheet voltage-space values are obtained by multiplying by $`K/R`$. The integrator state $`x_I`$ accumulates position error and requires the `pos` input; controller gains require a controller input and a positive [motorconst](XMLreference.md). A value of 0 (the default) disables the respective feature. When positive, <span class="at-val">slewmax</span> limits the rate-of-change of the first input (position setpoint in rad/s, or with signatures lacking `pos`, velocity setpoint or torque feedforward), <span class="at-val">Imax</span> clamps the integrator state (anti-windup), and <span class="at-val">Vmax</span> clamps the controller's drive voltage $`v_{\max}`$ (Volt). It does not bound the raw `voltage` input, which is added downstream: use <span class="at">ctrlrange</span> to limit a voltage command. (see [tech note](_static/dcmotor.pdf), Section 2.5)


#### <span class="el-prefix">actuator/</span> ⁠ **plugin** `dot`

Associate this actuator with an [engine plugin](programming/extension.md). Either <span class="at">plugin</span> or <span class="at">instance</span> are required.


<span class="at">plugin</span>: <span class="at-val">string, optional</span>  
Plugin identifier, used for implicit plugin instantiation.



<span class="at">instance</span>: <span class="at-val">string, optional</span>  
Instance name, used for explicit plugin instantiation.



<span class="at">dyntype</span>: <span class="at-val">\[none, integrator, filter, filterexact, pid, dcmotor, muscle, user\], "none"</span>  
Activation dynamics type for the actuator. The available dynamics types were already described in the [Actuation model](computation/index.md) section. If [dyntype](XMLreference.md) is not "none", an activation variable will be added to the actuator. This variable will be added after any activation state computed by the plugin (see [actuator plugin activations](programming/extension.md)).



<span class="at">actrange</span>: <span class="at-val">real(2), "0 0"</span>  
Range for clamping the activation state associated with this actuator's dyntype. The limit doesn't apply to activations computed by the plugin. The first value must be no greater than the second value. See the [Activation clamping](modeling.md) section for more details.






















































<span class="at">name</span>, <span class="at">class</span>, <span class="at">group</span>, <span class="at">delay</span>, <span class="at">actlimited</span>, <span class="at">ctrllimited</span>, <span class="at">forcelimited</span>, <span class="at">ctrlrange</span>, <span class="at">forcerange</span>, <span class="at">lengthrange</span>, <span class="at">gear</span>, <span class="at">cranklength</span>, <span class="at">joint</span>, <span class="at">jointinparent</span>, <span class="at">site</span>, <span class="at">tendon</span>, <span class="at">cranksite</span>, <span class="at">slidersite</span>, <span class="at">user</span>, <span class="at">actdim</span>, <span class="at">dynprm</span>, <span class="at">actearly</span>, <span class="at">damping</span>, <span class="at">armature</span>  
Same as in actuator/ [general](XMLreference.md).

### **sensor** ​

This is a grouping element for sensor definitions. It does not have attributes. The outputs of all sensors are concatenated in the field mjData.sensordata which has size mjModel.nsensordata. This data is not used in any internal computations.

In addition to the sensors created with the elements below, the top-level function *mj_step* computes the quantities mjData.cacc, mjData.cfrc_int and mjData.crfc_ext corresponding to body accelerations and interaction forces. Some of these quantities are used to compute the output of certain sensors (force, acceleration, etc.) but even if no such sensors are defined in the model, these quantities themselves are "features" that could be of interest to the user.

#### <span class="el-prefix">sensor/</span> ⁠ **touch** ​

This element creates a touch sensor. The active sensor zone is defined by a site. If a contact point falls within the site's volume, and involves a geom attached to the same body as the site, the corresponding contact force is included in the sensor reading. If a contact point falls outside the sensor zone, but the normal ray intersects the sensor zone, it is also included. This re-projection feature is needed because, without it, the contact point may leave the sensor zone from the back (due to soft contacts) and cause an erroneous force reading. The output of this sensor is a non-negative scalar. It is computed by adding up the (scalar) normal forces from all included contacts.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, required</span>  
Site defining the active sensor zone.


#### <span class="el-prefix">sensor/</span> ⁠ **accelerometer** ​

This element creates a 3-axis accelerometer. The sensor is mounted at a site, and has the same position and orientation as the site frame. This sensor outputs three numbers, which are the linear acceleration of the site (including gravity) in local coordinates.

The presence of this sensor in a model triggers a call to *mj_rnePostConstraint* during sensor computation.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, required</span>  
Site where the sensor is mounted. The accelerometer is centered and aligned with the site local frame.


#### <span class="el-prefix">sensor/</span> ⁠ **velocimeter** ​

This element creates a 3-axis velocimeter. The sensor is mounted at a site, and has the same position and orientation as the site frame. This sensor outputs three numbers, which are the linear velocity of the site in local coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, required</span>  
Site where the sensor is mounted. The velocimeter is centered and aligned with the site local frame.


#### <span class="el-prefix">sensor/</span> ⁠ **gyro** ​

This element creates a 3-axis gyroscope. The sensor is mounted at a site, and has the same position and orientation as the site frame. This sensor outputs three numbers, which are the angular velocity of the site in local coordinates. This sensor is often used in conjunction with an [accelerometer](XMLreference.md) mounted at the same site, to simulate an inertial measurement unit (IMU).









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, required</span>  
Site where the sensor is mounted. The gyroscope is centered and aligned with the site local frame.


#### <span class="el-prefix">sensor/</span> ⁠ **force** ​

This element creates a 3-axis force sensor. The sensor outputs three numbers, which are the interaction force between a child and a parent body, expressed in the site frame defining the sensor. The convention is that the site is attached to the child body, and the force points from the child towards the parent. The computation here takes into account all forces acting on the system, including contacts as well as external perturbations. Using this sensor often requires creating a dummy body welded to its parent (i.e., having no joint elements).

The presence of this sensor in a model triggers a call to *mj_rnePostConstraint* during sensor computation.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, required</span>  
Site where the sensor is mounted. The measured interaction force is between the body where the site is defined and its parent body, and points from the child towards the parent. The physical sensor being modeled could of course be attached to the parent body, in which case the sensor data would have the opposite sign. Note that each body has a unique parent but can have multiple children, which is why we define this sensor through the child rather than the parent body in the pair.


#### <span class="el-prefix">sensor/</span> ⁠ **torque** ​

This element creates a 3-axis torque sensor. This is similar to the [force](XMLreference.md) sensor above, but measures torque rather than force.

The presence of this sensor in a model triggers a call to *mj_rnePostConstraint* during sensor computation.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, required</span>  
Site where the sensor is mounted. The measured interaction torque is between the body where the site is defined and its parent body.


#### <span class="el-prefix">sensor/</span> ⁠ **magnetometer** ​

This element creates a magnetometer. It measures the magnetic flux at the sensor site position, expressed in the sensor site frame. The output is a 3D vector.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, required</span>  
The site where the sensor is attached.


#### <span class="el-prefix">sensor/</span> ⁠ **rangefinder** ​

This element creates a rangefinder.

- If associated with a [site](XMLreference.md), it measures the distance to the nearest geom surface, along the ray defined by the positive Z-axis of the site.
- If associated with a [camera](XMLreference.md), it outputs one distance measurement for each pixel in the camera image. Note that cameras face the [negative Z-axis](XMLreference.md) of their frame. The number of measurements in this case is equal to product of the camera's width and height [resolutions](XMLreference.md).

[<img src="images/XMLreference/rfcamera.png" class="align-right" style="width:45.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/sensor/rfcamera.xml)

If a ray does not intersect any geom surface, the sensor output is -1. If the origin of the ray is inside a geom, the surface is still detected. Geoms attached to the same body as the sensor site/camera are excluded. Invisible geoms, defined as geoms whose rgba (or whose material rgba) has alpha=0, are also excluded. Note however that geoms made invisible in the visualizer by disabling their geom group are not excluded; this is because sensor calculations are independent of the visualizer.

The image on the right (click to see the model being visualized) shows two rangefinder sensors attached to a perspective and an orthographic camera, with frustums visualized. Both cameras have 4x4 resolution, for 16 rays each. The rangefinder sensors report <span class="at">data</span> = <span class="at-val">"dist point normal"</span> (see below), so we can see the rays (lines), the intersection points (spheres) and the surface normals (arrows).


<span class="at">data</span>: <span class="at-val">\[dist, dir, origin, point, normal, depth\], "dist"</span>  
By default, the rangefinder outputs a distance measurement, as described above. However, it is also possible to specify a set of output data fields. The <span class="at">data</span> attribute can contain **multiple sequential data types**, as long as the relative order---as listed above---is maintained. For example, <span class="at">data</span> = <span class="at-val">"dist point normal"</span> will return 7 numbers per ray, while <span class="at">data</span> = <span class="at-val">"point origin"</span> is an error because <span class="at-val">origin</span> must come before <span class="at-val">point</span>.

- <span class="at-val">dist</span> **real(1)**: The distance from the ray origin to the nearest geom surface, -1 if no surface was hit. If this data type is included, rays will be visualized as lines.
- <span class="at-val">dir</span> **real(3)**: Normalized direction of the ray, or (0, 0, 0) if no surface was hit.
- <span class="at-val">origin</span> **real(3)**: The point from which the ray emanates (global frame). For sites and perspective cameras, this is the site/camera xpos. However for orthographic cameras, ray origins are spatially distributed along the image plane.
- <span class="at-val">point</span> **real(3)**: The point where the ray intersects the nearest geom surface in the global frame, or (0, 0, 0) if no surface was hit. If this data type is included, intersection points will be visualized as spheres.
- <span class="at-val">normal</span>: **real(3)**: The geom surface normal at the point where the ray intersects it, in the global frame, or (0, 0, 0) if no surface was hit. Note that normals always point towards the outside of the geom surface, regardless of the ray origin. If this data type is included along with either <span class="at-val">dist</span> or <span class="at-val">point</span>, normals will be visualized as arrows at the intersection points.
- <span class="at-val">depth</span>: **real(1)**: The distance of the hit point from the camera plane, -1 if no surface was hit. Note that this depth semantic corresponds to depth images in the computer graphics sense.










<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">site</span>: <span class="at-val">string, optional</span>  
The site where the sensor is attached.



<span class="at">camera</span>: <span class="at-val">string, optional</span>  
The camera where the sensor is attached.


#### <span class="el-prefix">sensor/</span> ⁠ **camprojection** ​

This element creates a camera projection sensor: the location of a target site, projected onto a camera image in pixel coordinates. The pixel origin (0, 0) is located at the top-left corner. Values are not clipped, so targets which fall outside the camera image will take values above or below the pixel range limits. Moreover, points behind the camera are also projected onto the image, so it is up to the user to filter out such points, if desired. This can be done using a [framepos](XMLreference.md) sensor with the camera as a reference frame: a negative/positive value in the z-coordinate indicates a location in front of/behind the camera plane, respectively.


<span class="at">site</span>: <span class="at-val">string, required</span>  
The site which is projected on to the camera image.



<span class="at">camera</span>: <span class="at-val">string, required</span>  
The camera used for the projection, its [resolution](XMLreference.md) attribute must be positive.










<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).









#### <span class="el-prefix">sensor/</span> ⁠ **jointpos** ​

This and the remaining sensor elements do not involve sensor-specific computations. Instead they copy into the array mjData.sensordata quantities that are already computed. This element creates a joint position or angle sensor. It can be attached to scalar joints (slide or hinge). Its output is scalar.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The joint whose position or angle will be sensed. Only scalar joints can be referenced here. The sensor output is copied from mjData.qpos.


#### <span class="el-prefix">sensor/</span> ⁠ **jointvel** ​

This element creates a joint velocity sensor. It can be attached to scalar joints (slide or hinge). Its output is scalar.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The joint whose velocity will be sensed. Only scalar joints can be referenced here. The sensor output is copied from mjData.qvel.


#### <span class="el-prefix">sensor/</span> ⁠ **tendonpos** ​

This element creates a tendon length sensor. It can be attached to both spatial and fixed tendons. Its output is scalar.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">tendon</span>: <span class="at-val">string, required</span>  
The tendon whose length will be sensed. The sensor output is copied from mjData.ten_length.


#### <span class="el-prefix">sensor/</span> ⁠ **tendonvel** ​

This element creates a tendon velocity sensor. It can be attached to both spatial and fixed tendons. Its output is scalar.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">tendon</span>: <span class="at-val">string, required</span>  
The tendon whose velocity will be sensed. The sensor output is copied from mjData.ten_velocity.


#### <span class="el-prefix">sensor/</span> ⁠ **actuatorpos** ​

This element creates an actuator length sensor. Recall that each actuator has a transmission which has length. This sensor can be attached to any actuator. Its output is scalar.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">actuator</span>: <span class="at-val">string, required</span>  
The actuator whose transmission's length will be sensed. The sensor output is copied from mjData.actuator_length.


#### <span class="el-prefix">sensor/</span> ⁠ **actuatorvel** ​

This element creates an actuator velocity sensor. This sensor can be attached to any actuator. Its output is scalar.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">actuator</span>: <span class="at-val">string, required</span>  
The actuator whose transmission's velocity will be sensed. The sensor output is copied from mjData.actuator_velocity.


#### <span class="el-prefix">sensor/</span> ⁠ **actuatorfrc** ​

This element creates an actuator force sensor. The quantity being sensed is the scalar actuator force, not the generalized force contributed by the actuator (the latter is the product of the scalar force and the vector of moment arms determined by the transmission). This sensor can be attached to any actuator. Its output is scalar.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">actuator</span>: <span class="at-val">string, required</span>  
The actuator whose scalar force output will be sensed. The sensor output is copied from mjData.actuator_force.


#### <span class="el-prefix">sensor/</span> ⁠ **jointactuatorfrc** ​

This element creates an actuator force sensor, measured at a joint. The quantity being sensed is the generalized force contributed by all actuators to a single scalar joint (hinge or slider). If the joint's [actuatorgravcomp](XMLreference.md) attribute is "true", this sensor will also measure contributions by gravity compensation forces (which are added directly to the joint and would *not* register in the [actuatorfrc](XMLreference.md)) sensor. This type of sensor is important when multiple actuators act on a single joint or when a single actuator acts on multiple joints. See [Force limits](modeling.md) for details.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The joint where actuator forces will be sensed. The sensor output is copied from `mjData.qfrc_actuator`.


#### <span class="el-prefix">sensor/</span> ⁠ **tendonactuatorfrc** ​

This element creates an actuator force sensor, measured at a tendon. The quantity being sensed is the total force contributed by all actuators to a single tendon. This type of sensor is important when multiple actuators act on a single tendon. See [Force limits](modeling.md) for details.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">tendon</span>: <span class="at-val">string, required</span>  
The tendon where actuator forces will be sensed.


#### <span class="el-prefix">sensor/</span> ⁠ **ballquat** ​

This element creates a quaternion sensor for a ball joints. It outputs 4 numbers corresponding to a unit quaternion.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The ball joint whose quaternion is sensed. The sensor output is copied from mjData.qpos.


#### <span class="el-prefix">sensor/</span> ⁠ **ballangvel** ​

This element creates a ball joint angular velocity sensor. It outputs 3 numbers corresponding to the angular velocity of the joint. The norm of that vector is the rotation speed in rad/s and the direction is the axis around which the rotation takes place.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The ball joint whose angular velocity is sensed. The sensor output is copied from mjData.qvel.


#### <span class="el-prefix">sensor/</span> ⁠ **jointlimitpos** ​

This element creates a joint limit sensor for position.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The joint whose limit is sensed. The sensor output equals mjData.efc_pos - mjData.efc_margin for the corresponding limit constraint. Note that the result is negative if the limit is violated, regardless of which side of the limit is violated. If both sides of the limit are violated simultaneously, only the first component is returned. If there is no violation, the result is 0.


#### <span class="el-prefix">sensor/</span> ⁠ **jointlimitvel** ​

This element creates a joint limit sensor for velocity.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The joint whose limit is sensed. The sensor output is copied from mjData.efc_vel. If the joint limit is not violated, the result is 0.


#### <span class="el-prefix">sensor/</span> ⁠ **jointlimitfrc** ​

This element creates a joint limit sensor for constraint force.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">joint</span>: <span class="at-val">string, required</span>  
The joint whose limit is sensed. The sensor output is copied from mjData.efc_force. If the joint limit is not violated, the result is 0.


#### <span class="el-prefix">sensor/</span> ⁠ **tendonlimitpos** ​

This element creates a tendon limit sensor for position.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">tendon</span>: <span class="at-val">string, required</span>  
The tendon whose limit is sensed. The sensor output equals mjData.efc_pos - mjData.efc_margin for the corresponding limit constraint. If the tendon limit is not violated, the result is 0.


#### <span class="el-prefix">sensor/</span> ⁠ **tendonlimitvel** ​

This element creates a tendon limit sensor for velocity.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">tendon</span>: <span class="at-val">string, required</span>  
The tendon whose limit is sensed. The sensor output is copied from mjData.efc_vel. If the tendon limit is not violated, the result is 0.


#### <span class="el-prefix">sensor/</span> ⁠ **tendonlimitfrc** ​

This element creates a tendon limit sensor for constraint force.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">tendon</span>: <span class="at-val">string, required</span>  
The tendon whose limit is sensed. The sensor output is copied from mjData.efc_force. If the tendon limit is not violated, the result is 0.


#### <span class="el-prefix">sensor/</span> ⁠ **framepos** ​

This element creates a sensor that returns the 3D position of the spatial frame of the object, in global coordinates or optionally with respect to a given frame-of-reference.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
The type of object to which the sensor is attached. This must be an object type that has a spatial frame. "body" refers to the inertial frame of the body, while "xbody" refers to the regular frame of the body (usually centered at the joint with the parent body).



<span class="at">objname</span>: <span class="at-val">string, required</span>  
The name of the object to which the sensor is attached.



<span class="at">reftype</span>: <span class="at-val">\[body, xbody, geom, site, camera\]</span>  
The type of object to which the frame-of-reference is attached. The semantics are identical to the <span class="at">objtype</span> attribute. If <span class="at">reftype</span> and <span class="at">refname</span> are given, the sensor values will be measured with respect to this frame. If they are not given, sensor values will be measured with respect to the global frame.



<span class="at">refname</span>: <span class="at-val">string</span>  
The name of the object to which the frame-of-reference is attached.


#### <span class="el-prefix">sensor/</span> ⁠ **framequat** ​

This element creates a sensor that returns the unit quaternion specifying the orientation of the spatial frame of the object, in global coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">reftype</span>: <span class="at-val">\[body, xbody, geom, site, camera\]</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">refname</span>: <span class="at-val">string</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **framexaxis** ​

This element creates a sensor that returns the 3D unit vector corresponding to the X-axis of the spatial frame of the object, in global coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">reftype</span>: <span class="at-val">\[body, xbody, geom, site, camera\]</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">refname</span>: <span class="at-val">string</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **frameyaxis** ​

This element creates a sensor that returns the 3D unit vector corresponding to the Y-axis of the spatial frame of the object, in global coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">reftype</span>: <span class="at-val">\[body, xbody, geom, site, camera\]</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">refname</span>: <span class="at-val">string</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **framezaxis** ​

This element creates a sensor that returns the 3D unit vector corresponding to the Z-axis of the spatial frame of the object, in global coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">reftype</span>: <span class="at-val">\[body, xbody, geom, site, camera\]</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">refname</span>: <span class="at-val">string</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **framelinvel** ​

This element creates a sensor that returns the 3D linear velocity of the spatial frame of the object, in global coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">reftype</span>: <span class="at-val">\[body, xbody, geom, site, camera\]</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">refname</span>: <span class="at-val">string</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **frameangvel** ​

This element creates a sensor that returns the 3D angular velocity of the spatial frame of the object, in global coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">reftype</span>: <span class="at-val">\[body, xbody, geom, site, camera\]</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">refname</span>: <span class="at-val">string</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **framelinacc** ​

This element creates a sensor that returns the 3D linear acceleration of the spatial frame of the object, in global coordinates.

The presence of this sensor in a model triggers a call to *mj_rnePostConstraint* during sensor computation.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **frameangacc** ​

This element creates a sensor that returns the 3D angular acceleration of the spatial frame of the object, in global coordinates.

The presence of this sensor in a model triggers a call to *mj_rnePostConstraint* during sensor computation.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
See [framepos](XMLreference.md) sensor.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
See [framepos](XMLreference.md) sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **subtreecom** ​

This element creates sensor that returns the center of mass of the kinematic subtree rooted at a specified body, in global coordinates.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">body</span>: <span class="at-val">string, required</span>  
Name of the body where the kinematic subtree is rooted.


#### <span class="el-prefix">sensor/</span> ⁠ **subtreelinvel** ​

This element creates sensor that returns the linear velocity of the center of mass of the kinematic subtree rooted at a specified body, in global coordinates.

The presence of this sensor in a model triggers a call to *mj_subtreeVel* during sensor computation.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">body</span>: <span class="at-val">string, required</span>  
Name of the body where the kinematic subtree is rooted.


#### <span class="el-prefix">sensor/</span> ⁠ **subtreeangmom** ​

This element creates sensor that returns the angular momentum around the center of mass of the kinematic subtree rooted at a specified body, in global coordinates.

The presence of this sensor in a model triggers a call to *mj_subtreeVel* during sensor computation.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">body</span>: <span class="at-val">string, required</span>  
Name of the body where the kinematic subtree is rooted.


#### <span class="el-prefix">sensor/</span> ⁠ **insidesite** ​

This element creates a sensor that returns 1 if the given object is inside a site, 0 otherwise. It is useful for triggering events in surrounding environment logic. See [example model](https://github.com/google-deepmind/mujoco/blob/main/test/engine/testdata/sensor/insidesite.xml).









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).










<span class="at">objtype</span>: <span class="at-val">\[body, xbody, geom, site, camera\], required</span>  
The type of the object to be queried. When <span class="at">enclosed</span> is `"false"`, this specifies the coordinate frame whose origin is checked (see [framepos](XMLreference.md)). When <span class="at">enclosed</span> is `"true"`, `body` checks all geoms directly attached to the body, `xbody` checks all geoms in the kinematic subtree rooted at the body, and `camera` is not supported.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
The name of the object to be queried. See [framepos](XMLreference.md).



<span class="at">site</span>: <span class="at-val">string</span>  
The site defining the volume used for the inside check.



<span class="at">enclosed</span>: <span class="at-val">bool, "false"</span>  
If true, checks full geometric enclosure instead of only checking whether the frame origin is inside the site. The sensor measures how much the object juts out of the site (the directed Hausdorff distance): positive values indicate how far the furthest point protrudes outside the site boundary, while zero or negative values indicate the object is fully enclosed (with the magnitude representing clearance to the boundary). Both the site and all queried geoms/sites must be compact convex shapes. For `objtype="body"` or `objtype="xbody"`, the sensor returns the maximum value across all geoms on the body or in its kinematic subtree, respectively (at least one geom must be present).


#### collision sensors

The following 3 sensor types, [sensor/distance](XMLreference.md), [sensor/normal](XMLreference.md) and [sensor/fromto](XMLreference.md), respectively measure the distance, normal direction and line segment of the smallest signed distance between the surfaces of two geoms using the narrow-phase geom-geom colliders. The collision computation is always performed, independently of the standard collision [selection and filtering](computation/index.md) pipeline. These 3 sensors share some common properties:


different (correct) behavior under <span class="title-ref">nativeccd</span>

As explained in [Collision Detection](computation/index.md), distances are inaccurate when using the [legacy CCD pipeline](computation/index.md), and its use is discouraged.



<span class="at">cutoff</span>  
For most sensors, the <span class="at">cutoff</span> attribute simply defines a clipping operation on sensor values. For collision sensors, it defines the maximum distance at which collisions will be detected, corresponding to the `dismax` argument of *mj_geomDistance*. For example, at the default value of 0, only negative distances (corresponding to geom-geom penetration) will be reported by [sensor/distance](XMLreference.md). In order to determine collision properties of non-penetrating geom pairs, a positive <span class="at">cutoff</span> is required.

<span class="at">geom1</span>, <span class="at">geom2</span>, <span class="at">body1</span>, <span class="at">body2</span>  
For all 3 collision sensor types, the two colliding geoms can be specified explicitly using the <span class="at">geom1</span> and <span class="at">geom2</span> attributes or implicitly, using <span class="at">body1</span>, <span class="at">body2</span>. In the latter case the sensor will iterate over all geoms of the specified body or bodies (mixed specification like <span class="at">geom1</span>, <span class="at">body2</span> are allowed), and select the collision with the smallest signed distance.


#### <span class="el-prefix">sensor/</span> ⁠ **distance** ​

This element creates a sensor that returns the smallest signed distance between the surfaces of two geoms. See [collision sensors](XMLreference.md) for more details about sensors of this type.


<span class="at">cutoff</span>  
See [collision sensors](XMLreference.md) for the semantics of this attribute, which is different than for other sensor categories. If no collision is detected, the distance sensor returns the <span class="at">cutoff</span> value, so in this case <span class="at">cutoff</span> acts as a maximum clipping value, in addition to the special semantics.



<span class="at">geom1</span>: <span class="at-val">string, optional</span>  
Name of the first geom. Exactly one of (<span class="at">geom1</span>, <span class="at">body1</span>) must be specified.



<span class="at">geom2</span>: <span class="at-val">string, optional</span>  
Name of the second geom. Exactly one of (<span class="at">geom2</span>, <span class="at">body2</span>) must be specified.



<span class="at">body1</span>: <span class="at-val">string, optional</span>  
Name of the first body. Exactly one of (<span class="at">geom1</span>, <span class="at">body1</span>) must be specified.



<span class="at">body2</span>: <span class="at-val">string, optional</span>  
Name of the second body. Exactly one of (<span class="at">geom2</span>, <span class="at">body2</span>) must be specified.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>:  
See [Sensors](modeling.md).








#### <span class="el-prefix">sensor/</span> ⁠ **normal** ​

This element creates a sensor that returns the normal direction of the smallest signed distance between the surfaces of two geoms. It is guaranteed to point from the surface of geom1 to the surface of geom2, though note that in the case of penetration, this direction is generally in the opposite direction to that of the centroids. See [collision sensors](XMLreference.md) for more details about sensors of this type.


<span class="at">cutoff</span>  
See [collision sensors](XMLreference.md) for the semantics of this attribute, which is different than for other sensor categories. If no collision is detected, the [normal](XMLreference.md) sensor returns (0, 0, 0), otherwise it returns a normalized direction vector. For this sensor, <span class="at">cutoff</span> does not lead to any clamping.



<span class="at">geom1</span>: <span class="at-val">string, optional</span>  
Name of the first geom. Exactly one of (<span class="at">geom1</span>, <span class="at">body1</span>) must be specified.



<span class="at">geom2</span>: <span class="at-val">string, optional</span>  
Name of the second geom. Exactly one of (<span class="at">geom2</span>, <span class="at">body2</span>) must be specified.



<span class="at">body1</span>: <span class="at-val">string, optional</span>  
Name of the first body. Exactly one of (<span class="at">geom1</span>, <span class="at">body1</span>) must be specified.



<span class="at">body2</span>: <span class="at-val">string, optional</span>  
Name of the second body. Exactly one of (<span class="at">geom2</span>, <span class="at">body2</span>) must be specified.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>:  
See [Sensors](modeling.md).








#### <span class="el-prefix">sensor/</span> ⁠ **fromto** ​

This element creates a sensor that returns the segment defining the smallest signed distance between the surfaces of two geoms. The segment is defined by 6 numbers (x1, y1, z1, x2, y2, z2) corresponding to two points in the world frame. (x1, y1, z1) is on the surface of geom1, (x2, y2, z2) is on the surface of geom2. When this sensor is present and the [mjVIS_RANGEFINDER](APIreference/APItypes.md) visualization flag is set, segments will be visualized as rangefinder rays. See [collision sensors](XMLreference.md) for more details about sensors of this type.


<span class="at">cutoff</span>  
See [collision sensors](XMLreference.md) for the semantics of this attribute, which is different than for other sensor categories. If no collision is detected, the [fromto](XMLreference.md) sensor returns 6 zeros. For this sensor, <span class="at">cutoff</span> does not lead to any clamping.



<span class="at">geom1</span>: <span class="at-val">string, optional</span>  
Name of the first geom. Exactly one of (<span class="at">geom1</span>, <span class="at">body1</span>) must be specified.



<span class="at">geom2</span>: <span class="at-val">string, optional</span>  
Name of the second geom. Exactly one of (<span class="at">geom2</span>, <span class="at">body2</span>) must be specified.



<span class="at">body1</span>: <span class="at-val">string, optional</span>  
Name of the first body. Exactly one of (<span class="at">geom1</span>, <span class="at">body1</span>) must be specified.



<span class="at">body2</span>: <span class="at-val">string, optional</span>  
Name of the second body. Exactly one of (<span class="at">geom2</span>, <span class="at">body2</span>) must be specified.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>:  
See [Sensors](modeling.md).








#### <span class="el-prefix">sensor/</span> ⁠ **contact** ​

**Motivation:** The array of contacts which occur during the main dynamics pipeline is inherently variable-sized. The purpose of the contact sensor is to report contact-related information in a fixed-size array. This is useful as input to learning-based agents and in environment logic.

Unlike the purely geometric [collision sensors](XMLreference.md) that act independently of the dynamics pipeline, the contact sensor reports information that was discovered during the collision and constraint steps, extracting data from `mjData.{contact, efc_force}`. Contacts in `mjData.contact` that are excluded from constraint force computation (for example, within the [gap](XMLreference.md) zone) are still matched and reported, with zero force and torque.

Contact sensor output involves three stages: **matching**, **reduction**, and **extraction**.

Matching  
Selects a set of contacts from `mjData.contact` using criteria defined by [geom1](XMLreference.md), [geom2](XMLreference.md), [body1](XMLreference.md), [body2](XMLreference.md), [subtree1](XMLreference.md), [subtree2](XMLreference.md) and [site](XMLreference.md). Matching applies an intersection of criteria, for example setting [body1](XMLreference.md) and [body2](XMLreference.md) will match contacts that involve both bodies, while setting only [geom1](XMLreference.md) will match any contacts involving that geom. Setting [site](XMLreference.md) will match contacts that are inside the volume defined by the site; this matching criterion can be used with {geom2, body2, subtree2}. The subtree attributes take a body name and match all contacts involving the body's subtree i.e., the body and all of its descendants. Setting [subtree1](XMLreference.md) and [subtree2](XMLreference.md) to the same body will match self-collisions in the subtree. Specifying no matching criterion will match all contacts.

Reduction  
Reduces the number of matched contacts to exactly [num](XMLreference.md) sub-arrays, or "slots". If less than <span class="at">num</span> contacts match, the remaining slots are set to be identically zero. Note that the default, "unsorted" reduction criterion is potentially non-deterministic. See [reduce](XMLreference.md) below.

Extraction  
Copies the set of fields specified by the user into each slot, see [data](XMLreference.md).



<span class="at">geom1</span>, <span class="at">geom2</span>: <span class="at-val">string, optional</span>  
Name of a geom participating in a contact. See **matching** [above](XMLreference.md).





<span class="at">body1</span>, <span class="at">body2</span>: <span class="at-val">string, optional</span>  
Name of a body participating in a contact. See **matching** [above](XMLreference.md).





<span class="at">subtree1</span>, <span class="at">subtree2</span>: <span class="at-val">string, optional</span>  
Name of a body whose subtree is participating in a contact. See **matching** [above](XMLreference.md).




<span class="at">site</span>: <span class="at-val">string, optional</span>  
Name of a site within whose volume the contact position must be found in order to match. See **matching** [above](XMLreference.md).



<span class="at">num</span>: <span class="at-val">int, "1"</span>  
Number of contacts to report. The sensor will always report <span class="at">num</span> sequential data arrays ("slots") per contact. The order in which contacts are reported depends on the [reduce](XMLreference.md) attribute.



<span class="at">data</span>: <span class="at-val">\[found, force, torque, dist, pos, normal, tangent, linvel, angvel\], "found"</span>  
Specification of which data field(s) to report from the selected contacts.

- <span class="at-val">found</span> **real(1)**: This field serves two purposes. First, it indicates whether a contact was found in this slot, 0 means not found while a positive number means found. Second, the positive value equals the number of *matching* contacts. So if <span class="at">num = 3</span> contacts were requested but only 2 were matched, the <span class="at-val">found</span> fields will equal (2, 2, 0); if 6 were matched they will equal (6, 6, 6).
- <span class="at-val">force</span> **real(3)**: The contact force, in the contact frame.
- <span class="at-val">torque</span> **real(3)**: The contact torque, in the contact frame.
- <span class="at-val">dist</span> **real(1)**: The penetration distance.
- <span class="at-val">pos</span>: **real(3)**: The contact position, in the global frame.
- <span class="at-val">normal</span>: **real(3)**: The contact normal direction, in the global frame.
- <span class="at-val">tangent</span>: **real(3)**: The first tangent direction, in the global frame. In order to complete the full 3x3 contact frame, use tangent2 = cross(normal, tangent).
- <span class="at-val">linvel</span>: **real(3)**: The relative linear velocity of the second contacting body with respect to the first at the contact position, expressed in the contact frame. Positive normal velocity (first component) corresponds to separation. Cannot be combined with `reduce="netforce"`.
- <span class="at-val">angvel</span>: **real(3)**: The relative angular velocity of the second contacting body with respect to the first, expressed in the contact frame. Cannot be combined with `reduce="netforce"`.

Importantly, the <span class="at">data</span> attribute can contain **multiple sequential data types**, as long as the relative order---as listed above---is maintained. For example, <span class="at">data</span> = <span class="at-val">"found force dist"</span> will return 5 numbers per contact (the concatenated values of \[found, force, dist\]), while <span class="at">data</span> = <span class="at-val">"force found dist"</span> is an error because <span class="at-val">found</span> must come before <span class="at-val">force</span>.

Missing contacts  
If less than <span class="at">num</span> contacts satisfy the matching criterion, the entire data slot is set to be identically zero. Because most data types can take 0 as a valid value, only the zero-ness of the <span class="at-val">normal</span> and <span class="at-val">tangent</span> unit vectors can be used to unambiguously detect an empty slot. For this reason, the <span class="at-val">found</span> data type is in place to allow for simple detection of missing contacts.

Size of sensordata block  
Unlike other sensors, the size of the corresponding sensordata block depends on the values of its attributes [num](XMLreference.md) and [data](XMLreference.md). The total size of the output of a contact sensor is the product `num x size(selected data fields)`. For example, requesting <span class="at">num = 6</span> contacts with <span class="at">data =</span> <span class="at-val">"force dist normal"</span> (3+1+3=7), will result in a sensordata block of 42 numbers (6 consecutive slots x 7 numbers per slot).

Direction convention  
Because contacts create two equal-and-opposite forces between contacting bodies, there is freedom in the choice of which body impinges on which.

The sensor's convention is for "geom1/body1/subtree1" and "geom2/body2/subtree2" to determine the direction of the normal. The normal always points from the first to the second.

In the case that a direction cannot be determined, as when only a <span class="at">site</span> is used as the matching criterion, or when both subtrees are the same, the normal direction is the same as it is in `mjData.contact`, where the normal points from the first to the second geom, and the two geoms are sorted according to their order in [mjtGeom](APIreference/APItypes.md).

Computation stage  
The computation stage (`sensor_needstage`) of a contact sensor depends on the requested <span class="at">data</span> fields and [reduce](XMLreference.md) criterion. If <span class="at">data</span> includes `force` or `torque`, or if <span class="at">reduce</span> is `maxforce` or `netforce`, the sensor is evaluated at `mjSTAGE_ACC`; otherwise, if <span class="at">data</span> includes `linvel` or `angvel`, it is evaluated at `mjSTAGE_VEL`; otherwise it is evaluated at `mjSTAGE_POS`.



<span class="at">reduce</span>: <span class="at-val">\[none, mindist, maxforce, netforce\], "none"</span>  
Reduction criterion to use. Also see **reduction** [above](XMLreference.md).

- **none**: Returns the first <span class="at">num</span> contacts that satisfy the matching criterion, in the order that they appear in `mjData.contact`. Note that while this is the fastest option, it is also potentially non-deterministic: future changes to collision detection code may cause the identity and order of matching contacts to change.
- **mindist**: Returns <span class="at">num</span> contacts with the smallest penetration depth, ascending order.
- **maxforce**: Returns <span class="at">num</span> contacts with the largest force norm, descending order.
- **netforce**: This reduction criterion returns one new "synthetic" contact, located at the force-weighted centroid of all matched contacts. The frame of the contact is the global frame, so normal and tangent directions lose their natural semantic. The force and torque are computed such that a wrench applied at the computed position will have the same net effect as all the matching contacts combined. Note that this reduction criterion always returns exactly one contact.



<span class="at">cutoff</span>:  
This attribute is ignored.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>:  
See [Sensors](modeling.md).








#### <span class="el-prefix">sensor/</span> ⁠ **tactile** ​

[<img src="images/XMLreference/tactile.png" class="align-right" style="width:30.0%" alt="image" />](https://github.com/google-deepmind/mujoco/blob/main/model/tactile/tactile.xml)

The tactile sensor evaluates penetration depth and tangential sliding speeds across the vertices (taxels) of a <span class="at">mesh</span> positioned in a <span class="at">geom</span> frame. For a sensor mesh with $`N`$ vertices, the sensor outputs $`3N`$ values in three contiguous blocks of length $`N`$: non-negative penetration depth $`d \ge 0`$ (`0` when not in contact) and two tangential sliding speeds $`|v_{t_1}|, |v_{t_2}| \ge 0`$ (populated when the mesh defines 3 normal vectors per vertex, as in [builtin](XMLreference.md) `wedge` and `plate` meshes).

Because the sensor is activated by contacts on any geom in the same weld body, the sensor's <span class="at">geom</span> can be a non-colliding surface mesh (`contype="0" conaffinity="0"`) while primitive geoms on the body handle collisions:

``` xml
<asset>
  <mesh name="plate" builtin="plate" params="25 25" scale="0.04 0.04 0.005"/>
</asset>
<worldbody>
  <body name="pad">
    <geom type="box" size="0.04 0.04 0.005"/>
    <geom name="sensor_surface" type="mesh" mesh="plate" contype="0" conaffinity="0"/>
  </body>
</worldbody>
<sensor>
  <tactile geom="sensor_surface" mesh="plate"/>
</sensor>
```

Signed distance at each taxel is evaluated analytically for colliding primitives and via plugins for `sdf` geoms. Any `mesh` geom that may collide with the sensor requires precomputing an SDF octree (otherwise it is ignored by the sensor). Enable [mjsMesh.needsdf](APIreference/APItypes.md) on colliding meshes via [mjSpec](APIreference/APItypes.md) before compiling:

``` C
mjSpec* spec = mj_parseXML("model.xml", NULL, NULL, 0);
mjsMesh* mesh = mjs_asMesh(mjs_findElement(spec, mjOBJ_MESH, "object"));
mesh->needsdf = 1;
mjModel* m = mj_compile(spec, NULL);
```

**Visualization**

- **3D scene**: Enabling [mjVIS_CONTACTPOINT](APIreference/APItypes.md) shades active mesh triangles with RGB channels proportional to penetration depth (red) and tangential speeds (green, blue).
- **2D image sensor**: In `simulate`, any [user](XMLreference.md) sensor with `sensor_intprm = [width, height, 0]`, `dim = width * height * 3`, and a non-zero sequence byte in `sensordata[adr + dim - 1]` is rendered as an RGB image in the *Sensor* panel.

**Laplacian post-processing**

Optical tactile sensors on hardware observe lateral displacement of embedded markers or a printed pattern as an elastomer pad deforms. MuJoCo computes only the raw independent normal depth $`d(x, y)`$ and tangential speeds at each taxel; it does not perform elastomer post-processing internally. Spatial coupling across a clamped elastomer surface can be modeled in user code by solving the 2D Poisson equation with zero Dirichlet boundary conditions:

``` math
-\nabla^2 \phi(x, y) = d(x, y) \quad \text{in } \Omega, \qquad \phi = 0 \quad \text{on } \partial\Omega.
```

<img src="images/XMLreference/tactile_laplacian_light.svg" class="only-light only-lightalign-center" style="width:100.0%" alt="image" />

<img src="images/XMLreference/tactile_laplacian_dark.svg" class="only-dark only-darkalign-center" style="width:100.0%" alt="image" />

Discretizing $`-\nabla^2`$ with a 5-point stencil on an $`n_x \times n_y`$ grid gives a constant banded symmetric positive-definite system $`L \phi = d`$ with bandwidth `nband = nx + 1`. Factoring $`L`$ once at initialization with *mju_cholFactorBand* allows solving for $`\phi`$ at runtime via *mju_cholSolveBand* and taking central differences $`(\Delta x, \Delta y) = \alpha \nabla \phi`$ to warp a pattern $`I(x + \Delta x, y + \Delta y)`$:

``` C
// assemble and factor banded negative 2D Laplacian (-nabla^2) on an (nx x ny) grid
void makeLaplacian(mjtNum* L, int nx, int ny) {
  int n = nx * ny, nband = nx + 1;
  mju_zero(L, n * nband);
  for (int i = 0; i < ny; i++) {
    for (int j = 0; j < nx; j++) {
      int k = i*nx + j;
      L[k*nband + nx] = 4;
      if (j > 0) L[k*nband + nx - 1] = -1;
      if (i > 0) L[k*nband]          = -1;
    }
  }
  mju_cholFactorBand(L, n, nband, 0, 0, 0);
}

// solve Poisson equation (-nabla^2 phi = d) and compute lateral displacement
void tactileDisplacement(mjtNum* dx, mjtNum* dy, mjtNum* phi,
                         const mjtNum* L, const mjtNum* d,
                         int nx, int ny, mjtNum alpha) {
  mju_cholSolveBand(phi, L, d, nx * ny, nx + 1, 0);
  for (int i = 0; i < ny; i++) {
    for (int j = 0; j < nx; j++) {
      int k = i*nx + j;
      mjtNum px = (j < nx-1 ? phi[k+1]  : 0) - (j > 0 ? phi[k-1]  : 0);
      mjtNum py = (i < ny-1 ? phi[k+nx] : 0) - (i > 0 ? phi[k-nx] : 0);
      dx[k] = 0.5 * alpha * px;
      dy[k] = 0.5 * alpha * py;
    }
  }
}
```


<span class="at">geom</span>: <span class="at-val">string, required</span>  
Name of the geom to associate the tactile sensor with.



<span class="at">mesh</span>: <span class="at-val">string, required</span>  
Name of the mesh to associate the tactile sensor with.









<span class="at">name</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>:  
See [Sensors](modeling.md).








#### <span class="el-prefix">sensor/</span> ⁠ **e_potential** ​

This element creates sensor that returns the potential energy.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).









#### <span class="el-prefix">sensor/</span> ⁠ **e_kinetic** ​

This element creates sensor that returns the kinetic energy.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).









#### <span class="el-prefix">sensor/</span> ⁠ **clock** ​

This element creates sensor that returns the simulation time.









<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">nsample</span>, <span class="at">interval</span>, <span class="at">delay</span>, <span class="at">user</span>  
See [Sensors](modeling.md).









#### <span class="el-prefix">sensor/</span> ⁠ **user** ​

This element creates a user sensor. MuJoCo does not know how to compute the output of this sensor. Instead the user should install the callback [mjcb_sensor](APIreference/APIglobals.md) which is expected to fill in the sensor data in `mjData.sensordata`. The specification in the XML is used to allocate space for this sensor, and also determine which MuJoCo object it is attached to and what stage of computation it needs before the data can be computed. Note that the MuJoCo object referenced here can be a tuple, which in turn can reference a custom collection of MuJoCo objects -- for example several bodies whose center of mass is of interest.

If a user sensor is of [stage](XMLreference.md) "vel" or "acc", then *mj_subtreeVel* or *mj_rnePostConstraint* will be triggered, respectively.





<span class="at">name</span>, <span class="at">noise</span>, <span class="at">cutoff</span>, <span class="at">user</span>  
See [Sensors](modeling.md).






<span class="at">objtype</span>: <span class="at-val">(any element type that can be named), optional</span>  
Type of the MuJoCo object to which the sensor is attached. This together with the objname attribute determines the actual object. If unspecified, will be [mjOBJ_UNKNOWN](APIreference/APItypes.md).



<span class="at">objname</span>: <span class="at-val">string, optional</span>  
Name of the MuJoCo object to which the sensor is attached.



<span class="at">datatype</span>: <span class="at-val">\[real, positive, axis, quaternion\], "real"</span>  
The type of output generated by this sensor. "axis" means a unit-length 3D vector. "quat" means a unit quaternion. These need to be declared because when MuJoCo adds noise, it must respect the vector normalization. "real" means a generic array (or scalar) of real values to which noise can be added independently.



<span class="at">needstage</span>: <span class="at-val">\[pos, vel, acc\], "acc"</span>  
The MuJoCo computation stage that must be completed before the user callback mjcb_sensor() is able to evaluate the output of this sensor.



<span class="at">dim</span>: <span class="at-val">int, required</span>  
Number of scalar outputs of this sensor.


#### <span class="el-prefix">sensor/</span> ⁠ **plugin** `dot`

Ascociate this sensor with an [engine plugin](programming/extension.md). Either <span class="at">plugin</span> or <span class="at">instance</span> are required.


<span class="at">plugin</span>: <span class="at-val">string, optional</span>  
Plugin identifier, used for implicit plugin instantiation.



<span class="at">instance</span>: <span class="at-val">string, optional</span>  
Instance name, used for explicit plugin instantiation.
















<span class="at">name</span>, <span class="at">cutoff</span>, <span class="at">objtype</span>, <span class="at">objname</span>, <span class="at">reftype</span>, <span class="at">refname</span>, <span class="at">user</span>  
See [Sensors](modeling.md).

### **keyframe** ​

This is a grouping element for keyframe definitions. It does not have attributes. Keyframes can be used to create a library of states that are of interest to the user, and to initialize the simulation state to one of the states in the library. They are not needed by any MuJoCo computations. The number of keyframes allocated in mjModel is the larger of the nkey attribute of [size](XMLreference.md), and the number of elements defined here. If fewer than nkey elements are defined here, the undefined keyframes have all their data set to 0, except for the qpos attribute which is set to mjModel.qpos0. The user can also set keyframe data in mjModel at runtime; this data will then appear in the saved MJCF model. Note that in [simulate.cc](programming/samples.md) the simulation state can be copied into a selected keyframe and vice versa.

#### <span class="el-prefix">keyframe/</span> ⁠ **key** ​

This element sets the data for one of the keyframes. They are set in the order in which they appear here. If the number of elements specified in the given vectors is less than the size of the corresponding mjData array, missing entries will be set to their values in the default configuration.


<span class="at">name</span>: <span class="at-val">string, optional</span>  
Name of this keyframe.



<span class="at">time</span>: <span class="at-val">real, "0"</span>  
Simulation time, copied into mjData.time when the simulation state is set to this keyframe.



<span class="at">qpos</span>: <span class="at-val">real(mjModel.nq), default = mjModel.qpos0</span>  
Vector of joint positions, copied into mjData.qpos when the simulation state is set to this keyframe.



<span class="at">qvel</span>: <span class="at-val">real(mjModel.nq), "0 0 ..."</span>  
Vector of joint velocities, copied into mjData.qvel when the simulation state is set to this keyframe.



<span class="at">act</span>: <span class="at-val">real(mjModel.na), "0 0 ..."</span>  
Vector of actuator activations, copied into mjData.act when the simulation state is set to this keyframe.



<span class="at">ctrl</span>: <span class="at-val">real(mjModel.nu), "0 0 ..."</span>  
Vector of controls, copied into mjData.ctrl when the simulation state is set to this keyframe.



<span class="at">mpos</span>: <span class="at-val">real(3\*mjModel.nmocap), default = mjModel.body_pos</span>  
Vector of mocap body positions, copied into mjData.mocap_pos when the simulation state is set to this keyframe.



<span class="at">mquat</span>: <span class="at-val">real(4\*mjModel.nmocap), default = mjModel.body_quat</span>  
Vector of mocap body quaternions, copied into mjData.mocap_quat when the simulation state is set to this keyframe.



<span class="at">plastic</span>: <span class="at-val">real(mjModel.nplastic), default = initial plastic state</span>  
Vector of plastic states, copied into mjData.plastic when the simulation state is set to this keyframe.


### **visual** ​

This element is in one-to-one correspondence with the low level structure mjVisual contained in the field mjModel.vis of mjModel. The settings here affect the visualizer, or more precisely the abstract phase of visualization which yields a list of geometric entities for subsequent rendering. The settings here are global, in contrast with the element-specific visual settings. The global and element-specific settings refer to non-overlapping properties. Some of the global settings affect properties such as triangulation of geometric primitives that cannot be set per element. Other global settings affect the properties of decorative objects, i.e., objects such as contact points and force arrows which do not correspond to model elements. The visual settings are grouped semantically into several subsections. <br/> This element is a good candidate for the [file include](modeling.md) mechanism. One can create an XML file with coordinated visual settings corresponding to a "theme", and then include this file in multiple models.

#### <span class="el-prefix">visual/</span> ⁠ **global** `dot`

While all settings in mjVisual are global, the settings here could not be fit into any of the other subsections. So this is effectively a miscellaneous subsection.


<span class="at">cameraid</span>: <span class="at-val">int, "-1"</span>  
The id of the camera used when initially loading the model in the visualizer. The default value of -1 means the free camera. In order to specify a [modeled camera](XMLreference.md), use the camera's id as given by *mj_name2id*.



<span class="at">orthographic</span>: <span class="at-val">\[false, true\], "false"</span>  
Whether the free camera defaults to a perspective projection (the default) or an orthographic projection. The eye of an orthographic free or tracking camera is placed behind the model, using [statistic/center](XMLreference.md) and [statistic/extent](XMLreference.md), so that zooming in does not clip it. Objects that move far from both the model center and the lookat point can still end up behind the eye and be clipped.



<span class="at">fovy</span>: <span class="at-val">real, "45"</span>  
This attribute specifies the vertical field of view of the free camera (and tracking camera), i.e., the camera that is always available in the visualizer even if no cameras are explicitly defined in the model. In perspective projection it is the vertical opening angle in degrees (regardless of the global [compiler/angle](XMLreference.md) setting). In orthographic projection the vertical view height (the distance between the top and bottom frustum planes, in units of length) is computed from <span class="at">fovy</span> and the camera's distance to the lookat point so it matches the perspective view height at the lookat point; in the visualizer UI, the field of view control displays and edits this distance in units of length. In either projection, the horizontal field of view is computed automatically from the viewport aspect ratio and the vertical field of view. For modeled cameras defined in the model, see [camera/fovy](XMLreference.md) (where orthographic <span class="at">fovy</span> is specified directly in units of length).



<span class="at">ipd</span>: <span class="at-val">real, "0.068"</span>  
This attribute specifies the inter-pupilary distance of the free camera. It only affects the rendering in stereoscopic mode. The left and right viewpoints are offset by half of this value in the corresponding direction.



<span class="at">azimuth</span>: <span class="at-val">real, "90"</span>  
This attribute specifies the initial azimuth of the free camera around the vertical z-axis, in degrees. A value of 0 corresponds to looking in the positive x direction, while the default value of 90 corresponds to looking in the positive y direction. The look-at point itself is specified by the [statistic/center](XMLreference.md) attribute, while the distance from the look-at point is controlled by the [statistic/extent](XMLreference.md) attribute.



<span class="at">elevation</span>: <span class="at-val">real, "-45"</span>  
This attribute specifies the initial elevation of the free camera with respect to the lookat point. Note that since this is a rotation around a vector parallel to the camera's X-axis (right in pixel space), *negative* numbers correspond to moving the camera *up* from the horizontal plane, and vice-versa. The look-at point itself is specified by the [statistic/center](XMLreference.md) attribute, while the distance from the look-at point is controlled by the [statistic/extent](XMLreference.md) attribute.



<span class="at">linewidth</span>: <span class="at-val">real, "1"</span>  
This attribute specifies the line-width in the sense of OpenGL. It affects the rendering in wire-frame mode.



<span class="at">glow</span>: <span class="at-val">real, "0.3"</span>  
The value of this attribute is added to the emission coefficient of all geoms attached to the selected body. As a result, the selected body appears to glow.



<span class="at">realtime</span>: <span class="at-val">real, "1"</span>  
This value sets the initial real-time factor of the model, when loaded in <span class="title-ref">simulate</span>. 1: real time. Less than 1: slower than real time. Must be greater than 0.



<span class="at">offwidth</span>: <span class="at-val">int, "640"</span>  
This and the next attribute specify the size in pixels of the off-screen OpenGL rendering buffer. This attribute specifies the width of the buffer. The size of this buffer can also be adjusted at runtime, but it is usually more convenient to set it in the XML.



<span class="at">offheight</span>: <span class="at-val">int, "480"</span>  
This attribute specifies the height in pixels of the OpenGL off-screen rendering buffer.



<span class="at">ellipsoidinertia</span>: <span class="at-val">\[false, true\], "false"</span>  
This attribute specifies how the equivalent inertia is visualized. "false": use box, "true": use ellipsoid.



<span class="at">bvactive</span>: <span class="at-val">\[false, true\], "false"</span>  
This attribute specifies whether collision and raycasting code should mark elements of Bounding Volume Hierarchies as intersecting, for the purpose of visualization. Setting this attribute to "true" can slow down simulation for models with high-resolution meshes, due to the O(N) cost of clearing visualization flags at each step.


#### <span class="el-prefix">visual/</span> ⁠ **quality** `dot`

This element specifies settings that affect the quality of the rendering. Larger values result in higher quality but possibly slower speed. Note that [simulate.cc](programming/samples.md) displays the frames per second (FPS). The target FPS is 60 Hz; if the number shown in the visualizer is substantially lower, this means that the GPU is over-loaded and the visualization should somehow be simplified.


<span class="at">shadowsize</span>: <span class="at-val">int, "4096"</span>  
This attribute specifies the size of the square texture used for shadow mapping. Higher values result in smoother shadows. The size of the area over which a [light](XMLreference.md) can cast shadows also affects smoothness, so these settings should be adjusted jointly. The default here is somewhat conservative. Most modern GPUs are able to handle significantly larger textures without slowing down.



<span class="at">offsamples</span>: <span class="at-val">int, "4"</span>  
This attribute specifies the number of multi-samples for anti-aliasing. Larger values produce better anti-aliasing but can slow down the GPU. Values less than or equal to 1 disable multi-sampling. In the [Filament renderer](programming/rendering.md), this attribute controls multi-sampling for window rendering and can be changed at runtime. In the classic OpenGL renderer, it only affects offscreen rendering; for window rendering, multi-sampling is specified in an OS-dependent way when the OpenGL context is first created, and cannot be changed from within MuJoCo. <br/> When rendering segmentation images, multi-sampling is automatically disabled so as not to average segmentation indices. However, some rendering backends ignore the automatic disabling. If your segmentation images contain bad indices, try manually setting this attribute to 0.



<span class="at">numslices</span>: <span class="at-val">int, "28"</span>  
This and the next three attributes specify the density of internally-generated meshes for geometric primitives. Such meshes are only used for rendering, while the collision detector works with the underlying analytic surfaces. This value is passed to the various visualizer functions as the "slices" parameter as used in GLU. It specifies the number of subdivisions around the Z-axis, similar to lines of longitude.



<span class="at">numstacks</span>: <span class="at-val">int, "16"</span>  
This value of this attribute is passed to the various visualization functions as the "stacks" parameter as used in GLU. It specifies the number of subdivisions along the Z-axis, similar to lines of latitude.



<span class="at">numquads</span>: <span class="at-val">int, "4"</span>  
This attribute specifies the number of rectangles for rendering box faces, automatically-generated planes (as opposed to geom planes which have an element-specific attribute with the same function), and sides of height fields. Even though a geometrically correct rendering can be obtained by setting this value to 1, illumination works better for larger values because we use per-vertex illumination (as opposed to per-fragment).


#### <span class="el-prefix">visual/</span> ⁠ **headlight** `dot`

This element is used to adjust the properties of the built-in headlight. The headlight is a directional light centered at the current camera and pointed in the direction in which the camera is looking. It does not cast shadows (which would be invisible anyway). Note that lights are additive, so when the headlight is enabled alongside explicit lights in the model, its intensity may need to be reduced. The headlight can be enabled or disabled by setting its [active](XMLreference.md) attribute.


<span class="at">ambient</span>: <span class="at-val">real(3), "0.1 0.1 0.1"</span>  
The ambient component of the headlight, in the sense of OpenGL. The alpha component here and in the next two attributes is set to 1 and cannot be adjusted.



<span class="at">diffuse</span>: <span class="at-val">real(3), "0.4 0.4 0.4"</span>  
The diffuse component of the headlight, in the sense of OpenGL.



<span class="at">specular</span>: <span class="at-val">real(3), "0.5 0.5 0.5"</span>  
The specular component of the headlight, in the sense of OpenGL.



<span class="at">active</span>: <span class="at-val">\[false, true, auto\], "auto"</span>  
This attribute enables or disables the headlight. (Note that integer values 0 ("false"), 1 ("true"), and 2 ("auto") are also accepted.) The default value of "auto" allows the runtime to decide whether or not the headlight should be enabled. For example, some tools can turn on the headlight if there are no other lights in the scene. For backwards compatibility, legacy renderers assume an "auto" headlight is always on.


#### <span class="el-prefix">visual/</span> ⁠ **map** `dot`

This element is used to specify scaling quantities that affect both the visualization and built-in mouse perturbations. Unlike the scaling quantities in the next element which are specific to spatial extent, the quantities here are miscellaneous.


<span class="at">stiffness</span>: <span class="at-val">real, "100"</span>  
This attribute controls the strength of mouse perturbations. The internal perturbation mechanism simulates a mass-spring-damper with critical damping, unit mass, and stiffness given here. Larger values mean that a larger force will be applied for the same displacement between the selected body and the mouse-controlled target.



<span class="at">stiffnessrot</span>: <span class="at-val">real, "500"</span>  
Same as above but applies to rotational perturbations rather than translational perturbations. Empirically, the rotational stiffness needs to be larger in order for rotational mouse perturbations to have an effect.



<span class="at">force</span>: <span class="at-val">real, "0.005"</span>  
This attributes controls the visualization of both contact forces and perturbation forces. The length of the rendered force vector equals the force magnitude multiplied by the value of this attribute and divided by the mean body mass for the model (see [statistic](XMLreference.md) element).



<span class="at">torque</span>: <span class="at-val">real, "0.1"</span>  
Same as above, but controls the rendering of contact torque and perturbation torque rather than force (currently disabled).



<span class="at">alpha</span>: <span class="at-val">real, "0.3"</span>  
When transparency is turned on in the visualizer, the geoms attached to all moving bodies are made more transparent. This is done by multiplying the geom-specific alpha values by this value.



<span class="at">fogstart</span>: <span class="at-val">real, "3"</span>  
The visualizer can simulate linear fog, in the sense of OpenGL. The start position of the fog is the model extent (see [statistic](XMLreference.md) element) multiplied by the value of this attribute.



<span class="at">fogend</span>: <span class="at-val">real, "10"</span>  
The end position of the fog is the model extent multiplied by the value of this attribute.



<span class="at">znear</span>: <span class="at-val">real, "0.01"</span>  
This and the next attribute determine the clipping planes of the OpenGL projection. The near clipping plane is particularly important: setting it too close causes (often severe) loss of resolution in the depth buffer, while setting it too far causes objects of interest to be clipped, making it impossible to zoom in. The distance to the near clipping plane is the model `extent` multiplied by the value of this attribute. Must be strictly positive.



<span class="at">zfar</span>: <span class="at-val">real, "50"</span>  
The distance to the far clipping plane is the model `extent` multiplied by the value of this attribute.



<span class="at">haze</span>: <span class="at-val">real, "0.3"</span>  
Proportion of the distance-to-horizon that is covered by haze (when haze rendering is enabled and a skybox is present).



<span class="at">shadowclip</span>: <span class="at-val">real, "1"</span>  
As mentioned above, shadow quality depends on the size of the shadow texture as well as the area where a given light can cast shadows. For directional lights, the area would be infinite unless we limited it somehow. This attribute specifies the limits, as +/- the model extent multiplied by the present value. These limits define a square in the plane orthogonal to the light direction. If a shadow crosses the boundary of this virtual square, it will disappear abruptly, revealing the edges of the square.



<span class="at">shadowscale</span>: <span class="at-val">real, "0.6"</span>  
This attribute plays a similar role as the previous one, but applies to spotlights rather than directional lights. Spotlights have a cutoff angle, limited internally to 80 deg. However this angle is often too large to obtain good quality shadows, and it is necessary to limit the shadow to a smaller cone. The angle of the cone in which shadows can be cast is the light cutoff multiplied by the present value.



<span class="at">actuatortendon</span>: <span class="at-val">real, "2"</span>  
Ratio of actuator width to tendon width for rendering of actuators attached to tendons.


#### <span class="el-prefix">visual/</span> ⁠ **scale** `dot`

The settings in this element control the spatial extent of various decorative objects. In all cases, the rendered size equals the mean body size (see [statistic](XMLreference.md) element) multiplied by the value of an attribute documented below.


<span class="at">forcewidth</span>: <span class="at-val">real, "0.1"</span>  
The radius of the arrows used to render contact forces and perturbation forces.



<span class="at">contactwidth</span>: <span class="at-val">real, "0.3"</span>  
The radius of the cylinders used to render contact points. The normal direction of the cylinder is aligned with the contact normal. Making the cylinder short and wide results in a "pancake" representation of the tangent plane.



<span class="at">contactheight</span>: <span class="at-val">real, "0.1"</span>  
The height of the cylinders used to render contact points.



<span class="at">connect</span>: <span class="at-val">real, "0.2"</span>  
The radius of the capsules used to connect bodies and joints, resulting in an automatically generated skeleton.



<span class="at">com</span>: <span class="at-val">real, "0.4"</span>  
The radius of the spheres used to render the centers of mass of kinematic sub-trees.



<span class="at">camera</span>: <span class="at-val">real, "0.3"</span>  
The size of the decorative object used to represent model cameras in the rendering.



<span class="at">light</span>: <span class="at-val">real, "0.3"</span>  
The size of the decorative object used to represent model lights in the rendering.



<span class="at">selectpoint</span>: <span class="at-val">real, "0.2"</span>  
The radius of the sphere used to render the selection point (i.e., the point where the user left-double-clicked to select a body). Note that the local and global coordinates of this point can be printed in the 3D view by activating the corresponding rendering flags. In this way, the coordinates of points of interest can be found.



<span class="at">jointlength</span>: <span class="at-val">real, "1.0"</span>  
The length of the arrows used to render joint axes.



<span class="at">jointwidth</span>: <span class="at-val">real, "0.1"</span>  
The radius of the arrows used to render joint axes.



<span class="at">actuatorlength</span>: <span class="at-val">real, "0.7"</span>  
The length of the arrows used to render actuators acting on scalar joints only.



<span class="at">actuatorwidth</span>: <span class="at-val">real, "0.2"</span>  
The radius of the arrows used to render actuators acting on scalar joints only.



<span class="at">framelength</span>: <span class="at-val">real, "1.0"</span>  
The length of the cylinders used to render coordinate frames. The world frame is automatically scaled relative to this setting.



<span class="at">framewidth</span>: <span class="at-val">real, "0.1"</span>  
The radius of the cylinders used to render coordinate frames.



<span class="at">constraint</span>: <span class="at-val">real, "0.1"</span>  
The radius of the capsules used to render violations in spatial constraints.



<span class="at">slidercrank</span>: <span class="at-val">real, "0.2"</span>  
The radius of the capsules used to render slider-crank mechanisms. The second part of the mechanism is automatically scaled relative to this setting.



<span class="at">frustum</span>: <span class="at-val">real, "10"</span>  
The distance of the zfar plane from the camera pinhole for rendering the frustum.


#### <span class="el-prefix">visual/</span> ⁠ **rgba** `dot`

The settings in this element control the color and transparency (rgba) of various decorative objects. We will call this combined attribute "color" to simplify terminology below. All values should be in the range \[0 1\]. An alpha value of 0 disables the rendering of the corresponding object.


<span class="at">fog</span>: <span class="at-val">real(4), "0 0 0 1"</span>  
When fog is enabled, the color of all pixels fades towards the color specified here. The spatial extent of the fading is controlled by the fogstart and fogend attributes of the [map](XMLreference.md) element above.



<span class="at">haze</span>: <span class="at-val">real(4), "1 1 1 1"</span>  
Haze color at the horizon, used to transition between an infinite plane and a skybox smoothly. The default creates white haze. To create a seamless transition, make sure the skybox colors near the horizon are similar to the plane color/texture, and set the haze color somewhere in that color gamut.



<span class="at">force</span>: <span class="at-val">real(4), "1 0.5 0.5 1"</span>  
Color of the arrows used to render perturbation forces.



<span class="at">inertia</span>: <span class="at-val">real(4), "0.8 0.2 0.2 0.6"</span>  
Color of the boxes used to render equivalent body inertias. This is the only rgba setting that has transparency by default, because it is usually desirable to see the geoms inside the inertia box.



<span class="at">joint</span>: <span class="at-val">real(4), "0.2 0.6 0.8 1"</span>  
Color of the arrows used to render joint axes. If a joint is limited and the joint value exceeds the limit, the value of the [constraint impedance](computation/index.md) $`d`$ is used to mix this color and [rgba/constraint](XMLreference.md).



<span class="at">actuator</span>: <span class="at-val">real(4), "0.2 0.25 0.2 1"</span>  
Actuator color for neutral value of the control.



<span class="at">actuatornegative</span>: <span class="at-val">real(4), "0.2 0.6 0.9 1"</span>  
Actuator color for most negative value of the control.



<span class="at">actuatorpositive</span>: <span class="at-val">real(4), "0.9 0.4 0.2 1"</span>  
Actuator color for most positive value of the control.



<span class="at">com</span>: <span class="at-val">real(4), "0.9 0.9 0.9 1"</span>  
Color of the spheres used to render sub-tree centers of mass.



<span class="at">camera</span>: <span class="at-val">real(4), "0.6 0.9 0.6 1"</span>  
Color of the decorative object used to represent model cameras in the rendering.



<span class="at">light</span>: <span class="at-val">real(4), "0.6 0.6 0.9 1"</span>  
Color of the decorative object used to represent model lights in the rendering.



<span class="at">selectpoint</span>: <span class="at-val">real(4), "0.9 0.9 0.1 1"</span>  
Color of the sphere used to render the selection point.



<span class="at">connect</span>: <span class="at-val">real(4), "0.2 0.2 0.8 1"</span>  
Color of the capsules used to connect bodies and joints, resulting in an automatically generated skeleton.



<span class="at">contactpoint</span>: <span class="at-val">real(4), "0.9 0.6 0.2 1"</span>  
Color of the cylinders used to render contact points.



<span class="at">contactforce</span>: <span class="at-val">real(4), "0.7 0.9 0.9 1"</span>  
Color of the arrows used to render contact forces. When splitting of contact forces into normal and tangential components is enabled, this color is used to render the normal components.



<span class="at">contactfriction</span>: <span class="at-val">real(4), "0.9 0.8 0.4 1"</span>  
Color of the arrows used to render contact tangential forces, only when splitting is enabled.



<span class="at">contacttorque</span>: <span class="at-val">real(4), "0.9 0.7 0.9 1"</span>  
Color of the arrows used to render contact torques (currently disabled).



<span class="at">contactgap</span>: <span class="at-val">real(4), "0.5 0.8 0.9 1"</span>  
Color of contacts that fall in the contact gap (and are thereby excluded from contact force computations).



<span class="at">rangefinder</span>: <span class="at-val">real(4), "1 1 0.1 1"</span>  
Color of line geoms used to render rangefinder sensors.



<span class="at">constraint</span>: <span class="at-val">real(4), "0.9 0 0 1"</span>  
Color corresponding to spatial constraint violations -- equality constraints, joint limits, and tendon limits.



<span class="at">slidercrank</span>: <span class="at-val">real(4), "0.5 0.3 0.8 1"</span>  
Color of slider-crank mechanisms.



<span class="at">crankbroken</span>: <span class="at-val">real(4), "0.9 0 0 1"</span>  
Color used to render the crank of slide-crank mechanisms, in model configurations where the specified rod length cannot be maintained, i.e., it is "broken".



<span class="at">frustum</span>: <span class="at-val">real(4), "1 1 0 0.2"</span>  
Color used to render the camera frustum.



<span class="at">bv</span>: <span class="at-val">real(4), "0 1 0 0.5"</span>  
Color used to render bounding volumes.



<span class="at">bvactive</span>: <span class="at-val">real(4), "1 0 0 0.5"</span>  
Color used to render active bounding volumes, if the [bvactive](XMLreference.md) flag is "true".


### **default** `sync`

This element is used to create a new defaults class; see [Default settings](modeling.md) above. Defaults classes can be nested, inheriting all attribute values from their parent. The top-level defaults class is always defined; it is called "main" if omitted.


<span class="at">class</span>: <span class="at-val">string, required (except at the top level)</span>  
The name of the defaults class. It must be unique among all defaults classes. This name is used to make the class active when creating an actual model element.


#### <span class="el-prefix">default/</span> ⁠ **mesh** `dot`<span id="default-mesh-maxhullvert"></span><span id="default-mesh-scale"></span><span id="default-mesh"></span>

This element sets the attributes of the dummy [mesh](XMLreference.md) element of the defaults class.\
The available attributes are: [scale](XMLreference.md) and [maxhullvert](XMLreference.md).

#### <span class="el-prefix">default/</span> ⁠ **texture** `dot`<span id="default-texture-nchannel"></span><span id="default-texture-vflip"></span><span id="default-texture-hflip"></span><span id="default-texture-height"></span><span id="default-texture-width"></span><span id="default-texture-random"></span><span id="default-texture-markrgb"></span><span id="default-texture-mark"></span><span id="default-texture-rgb2"></span><span id="default-texture-rgb1"></span><span id="default-texture-builtin"></span><span id="default-texture-gridlayout"></span><span id="default-texture-gridsize"></span><span id="default-texture-colorspace"></span><span id="default-texture-type"></span><span id="default-texture"></span>

This element sets the attributes of the dummy [texture](XMLreference.md) element of the defaults class.\
All texture attributes are available here except: name, class, content_type, file, fileright, fileleft, fileup, filedown, filefront, fileback.

#### <span class="el-prefix">default/</span> ⁠ **material** `dot`<span id="default-material-texrepeat"></span><span id="default-material-rgba"></span><span id="default-material-roughness"></span><span id="default-material-metallic"></span><span id="default-material-reflectance"></span><span id="default-material-shininess"></span><span id="default-material-specular"></span><span id="default-material-emission"></span><span id="default-material-texture"></span><span id="default-material"></span>

This element sets the attributes of the dummy [material](XMLreference.md) element of the defaults class.\
All material attributes are available here except: name, class.

#### <span class="el-prefix">default/</span> ⁠ **joint** `dot`<span id="default-joint-frictionloss"></span><span id="default-joint-damping"></span><span id="default-joint-armature"></span><span id="default-joint-springyield"></span><span id="default-joint-springref"></span><span id="default-joint-ref"></span><span id="default-joint-margin"></span><span id="default-joint-actuatorfrcrange"></span><span id="default-joint-range"></span><span id="default-joint-stiffness"></span><span id="default-joint-solimpfriction"></span><span id="default-joint-solreffriction"></span><span id="default-joint-solimplimit"></span><span id="default-joint-solreflimit"></span><span id="default-joint-actuatorgravcomp"></span><span id="default-joint-actuatorfrclimited"></span><span id="default-joint-limited"></span><span id="default-joint-springdamper"></span><span id="default-joint-axis"></span><span id="default-joint-pos"></span><span id="default-joint-group"></span><span id="default-joint-type"></span><span id="default-joint"></span>

This element sets the attributes of the dummy [joint](XMLreference.md) element of the defaults class.\
All joint attributes are available here except: name, class.

#### <span class="el-prefix">default/</span> ⁠ **geom** `dot`<span id="default-geom-fluidcoef"></span><span id="default-geom-fluidshape"></span><span id="default-geom-castshadow"></span><span id="default-geom-rgba"></span><span id="default-geom-fitscale"></span><span id="default-geom-mesh"></span><span id="default-geom-hfield"></span><span id="default-geom-euler"></span><span id="default-geom-zaxis"></span><span id="default-geom-xyaxes"></span><span id="default-geom-axisangle"></span><span id="default-geom-fromto"></span><span id="default-geom-adhesion"></span><span id="default-geom-surfacevel"></span><span id="default-geom-gap"></span><span id="default-geom-margin"></span><span id="default-geom-solimp"></span><span id="default-geom-solref"></span><span id="default-geom-solmix"></span><span id="default-geom-shellinertia"></span><span id="default-geom-density"></span><span id="default-geom-mass"></span><span id="default-geom-friction"></span><span id="default-geom-material"></span><span id="default-geom-size"></span><span id="default-geom-priority"></span><span id="default-geom-group"></span><span id="default-geom-condim"></span><span id="default-geom-conaffinity"></span><span id="default-geom-contype"></span><span id="default-geom-quat"></span><span id="default-geom-pos"></span><span id="default-geom-type"></span><span id="default-geom"></span>

This element sets the attributes of the dummy [geom](XMLreference.md) element of the defaults class.\
All geom attributes are available here except: name, class.

#### <span class="el-prefix">default/</span> ⁠ **site** `dot`<span id="default-site-rgba"></span><span id="default-site-euler"></span><span id="default-site-zaxis"></span><span id="default-site-xyaxes"></span><span id="default-site-axisangle"></span><span id="default-site-fromto"></span><span id="default-site-size"></span><span id="default-site-mesh"></span><span id="default-site-material"></span><span id="default-site-quat"></span><span id="default-site-pos"></span><span id="default-site-group"></span><span id="default-site-type"></span><span id="default-site"></span>

This element sets the attributes of the dummy [site](XMLreference.md) element of the defaults class.\
All site attributes are available here except: name, class.

#### <span class="el-prefix">default/</span> ⁠ **camera** `dot`<span id="default-camera-sensorsize"></span><span id="default-camera-principalpixel"></span><span id="default-camera-principal"></span><span id="default-camera-focalpixel"></span><span id="default-camera-focal"></span><span id="default-camera-user"></span><span id="default-camera-mode"></span><span id="default-camera-euler"></span><span id="default-camera-zaxis"></span><span id="default-camera-xyaxes"></span><span id="default-camera-axisangle"></span><span id="default-camera-quat"></span><span id="default-camera-pos"></span><span id="default-camera-ipd"></span><span id="default-camera-output"></span><span id="default-camera-resolution"></span><span id="default-camera-fovy"></span><span id="default-camera-projection"></span>

This element sets the attributes of the dummy [camera](XMLreference.md) element of the defaults class.\
All camera attributes are available here except: name, class, mode, target.

#### <span class="el-prefix">default/</span> ⁠ **light** `dot`<span id="default-light-exponent"></span><span id="default-light-softness"></span><span id="default-light-cutoff"></span><span id="default-light-attenuation"></span><span id="default-light-range"></span><span id="default-light-bulbradius"></span><span id="default-light-specular"></span><span id="default-light-ambient"></span><span id="default-light-intensity"></span><span id="default-light-diffuse"></span><span id="default-light-active"></span><span id="default-light-castshadow"></span><span id="default-light-directional"></span><span id="default-light-type"></span><span id="default-light-dir"></span><span id="default-light-pos"></span><span id="default-light"></span>

This element sets the attributes of the dummy [light](XMLreference.md) element of the defaults class.\
All light attributes are available here except: name, class.

#### <span class="el-prefix">default/</span> ⁠ **pair** `dot`<span id="default-pair-margin"></span><span id="default-pair-gap"></span><span id="default-pair-solimp"></span><span id="default-pair-solreffriction"></span><span id="default-pair-solref"></span><span id="default-pair-friction"></span><span id="default-pair-condim"></span><span id="default-pair"></span>

This element sets the attributes of the dummy [pair](XMLreference.md) element of the defaults class.\
All pair attributes are available here except: name, class, geom1, geom2.

#### <span class="el-prefix">default/</span> ⁠ **equality** `dot`<span id="default-equality-solref"></span><span id="default-equality-active"></span><span id="default-equality"></span>

This element sets the attributes of the dummy [equality](XMLreference.md) element of the defaults class. The actual equality constraints have types depending on the sub-element used to define them. However here we are setting attributes common to all equality constraint types, which is why we do not make a distinction between types.\
The equality sub-element attributes available here are: <span class="at">active</span>, <span class="at">solref</span>, <span class="at">solimp</span>.

#### <span class="el-prefix">default/</span> ⁠ **tendon** `dot`<span id="default-tendon-rgba"></span><span id="default-tendon-armature"></span><span id="default-tendon-damping"></span><span id="default-tendon-springyield"></span><span id="default-tendon-stiffness"></span><span id="default-tendon-margin"></span><span id="default-tendon-material"></span><span id="default-tendon-width"></span><span id="default-tendon-springlength"></span><span id="default-tendon-frictionloss"></span><span id="default-tendon-solimpfriction"></span><span id="default-tendon-solreffriction"></span><span id="default-tendon-solimplimit"></span><span id="default-tendon-solreflimit"></span><span id="default-tendon-actuatorfrcrange"></span><span id="default-tendon-range"></span><span id="default-tendon-actuatorfrclimited"></span><span id="default-tendon-limited"></span><span id="default-tendon-group"></span><span id="default-tendon"></span>

This element sets the attributes of the dummy [tendon](XMLreference.md) element of the defaults class. Similar to equality constraints, the actual tendons have types, but here we are setting attributes common to all types.\
All tendon sub-element attributes are available here except: name, class.

#### <span class="el-prefix">default/</span> ⁠ **general** `dot`<span id="default-general-input"></span><span id="default-general-inheritrange"></span><span id="default-general-ffrange"></span><span id="default-general-velrange"></span><span id="default-general-biasprm"></span><span id="default-general-gainprm"></span><span id="default-general-dynprm"></span><span id="default-general-biastype"></span><span id="default-general-gaintype"></span><span id="default-general-dyntype"></span><span id="default-general-actdim"></span><span id="default-general-interp"></span><span id="default-general-nsample"></span><span id="default-general-delay"></span><span id="default-general-group"></span><span id="default-general-user"></span><span id="default-general-cranklength"></span><span id="default-general-armature"></span><span id="default-general-damping"></span><span id="default-general-gear"></span><span id="default-general-actrange"></span><span id="default-general-forcerange"></span><span id="default-general-ctrlrange"></span><span id="default-general-actlimited"></span><span id="default-general-forcelimited"></span><span id="default-general-ctrllimited"></span><span id="default-general"></span>

This element sets the attributes of the dummy [general](XMLreference.md) element of the defaults class.\
All general attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **motor** `dot`<span id="default-motor-nsample"></span><span id="default-motor-delay"></span><span id="default-motor-group"></span><span id="default-motor-user"></span><span id="default-motor-cranklength"></span><span id="default-motor-armature"></span><span id="default-motor-damping"></span><span id="default-motor-gear"></span><span id="default-motor-forcerange"></span><span id="default-motor-ctrlrange"></span><span id="default-motor-forcelimited"></span><span id="default-motor-ctrllimited"></span><span id="default-motor"></span>

This and the following shortcut elements set the single actuator default of the class, see [Actuator shortcuts](modeling.md). Any actuator in the class inherits its mechanical attributes; the shortcut's own parameters are inherited only by actuators written with the same shortcut or with [general](XMLreference.md). Using more than one shortcut in the same defaults class is not useful, because each resets the gain, bias and dynamics parameters set by the previous one. All [motor](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **position** `dot`<span id="default-position-dampratio"></span><span id="default-position-kv"></span><span id="default-position-kp"></span><span id="default-position-interp"></span><span id="default-position-nsample"></span><span id="default-position-delay"></span><span id="default-position-group"></span><span id="default-position-user"></span><span id="default-position-cranklength"></span><span id="default-position-armature"></span><span id="default-position-damping"></span><span id="default-position-gear"></span><span id="default-position-forcerange"></span><span id="default-position-inheritrange"></span><span id="default-position-ctrlrange"></span><span id="default-position-forcelimited"></span><span id="default-position-ctrllimited"></span><span id="default-position"></span>

All [position](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **velocity** `dot`<span id="default-velocity-interp"></span><span id="default-velocity-nsample"></span><span id="default-velocity-delay"></span><span id="default-velocity-group"></span><span id="default-velocity-user"></span><span id="default-velocity-cranklength"></span><span id="default-velocity-armature"></span><span id="default-velocity-damping"></span><span id="default-velocity-gear"></span><span id="default-velocity-forcerange"></span><span id="default-velocity-ctrlrange"></span><span id="default-velocity-forcelimited"></span><span id="default-velocity-ctrllimited"></span><span id="default-velocity"></span>

All [velocity](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **intvelocity** `dot`<span id="default-intvelocity-kv"></span><span id="default-intvelocity-kp"></span><span id="default-intvelocity-interp"></span><span id="default-intvelocity-nsample"></span><span id="default-intvelocity-delay"></span><span id="default-intvelocity-group"></span><span id="default-intvelocity-user"></span><span id="default-intvelocity-cranklength"></span><span id="default-intvelocity-armature"></span><span id="default-intvelocity-damping"></span><span id="default-intvelocity-gear"></span><span id="default-intvelocity-inheritrange"></span><span id="default-intvelocity-actrange"></span><span id="default-intvelocity-forcerange"></span><span id="default-intvelocity-ctrlrange"></span><span id="default-intvelocity-actlimited"></span><span id="default-intvelocity-forcelimited"></span><span id="default-intvelocity-ctrllimited"></span><span id="default-intvelocity"></span>

All [intvelocity](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **pid** `dot`<span id="default-pid-slewmax"></span><span id="default-pid-imax"></span><span id="default-pid-ki"></span><span id="default-pid-dampratio"></span><span id="default-pid-kv"></span><span id="default-pid-kp"></span><span id="default-pid-delay"></span><span id="default-pid-interp"></span><span id="default-pid-nsample"></span><span id="default-pid-group"></span><span id="default-pid-user"></span><span id="default-pid-cranklength"></span><span id="default-pid-armature"></span><span id="default-pid-damping"></span><span id="default-pid-gear"></span><span id="default-pid-inheritrange"></span><span id="default-pid-forcerange"></span><span id="default-pid-ffrange"></span><span id="default-pid-velrange"></span><span id="default-pid-posrange"></span><span id="default-pid-ctrlrange"></span><span id="default-pid-forcelimited"></span><span id="default-pid-ctrllimited"></span><span id="default-pid"></span>

All [pid](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **orientation** `dot`<span id="default-orientation-dampratio"></span><span id="default-orientation-kv"></span><span id="default-orientation-kp"></span><span id="default-orientation-delay"></span><span id="default-orientation-interp"></span><span id="default-orientation-nsample"></span><span id="default-orientation-group"></span><span id="default-orientation-user"></span><span id="default-orientation-forcerange"></span><span id="default-orientation-ctrlrange"></span><span id="default-orientation-forcelimited"></span><span id="default-orientation"></span>

All [orientation](XMLreference.md) attributes are available here except: name, class, joint, site, refsite.

#### <span class="el-prefix">default/</span> ⁠ **damper** `dot`<span id="default-damper-interp"></span><span id="default-damper-nsample"></span><span id="default-damper-delay"></span><span id="default-damper-group"></span><span id="default-damper-user"></span><span id="default-damper-cranklength"></span><span id="default-damper-armature"></span><span id="default-damper-damping"></span><span id="default-damper-gear"></span><span id="default-damper-forcerange"></span><span id="default-damper-ctrlrange"></span><span id="default-damper-forcelimited"></span><span id="default-damper"></span>

All [damper](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **cylinder** `dot`<span id="default-cylinder-diameter"></span><span id="default-cylinder-area"></span><span id="default-cylinder-timeconst"></span><span id="default-cylinder-interp"></span><span id="default-cylinder-nsample"></span><span id="default-cylinder-delay"></span><span id="default-cylinder-group"></span><span id="default-cylinder-user"></span><span id="default-cylinder-cranklength"></span><span id="default-cylinder-armature"></span><span id="default-cylinder-damping"></span><span id="default-cylinder-gear"></span><span id="default-cylinder-forcerange"></span><span id="default-cylinder-ctrlrange"></span><span id="default-cylinder-forcelimited"></span><span id="default-cylinder-ctrllimited"></span><span id="default-cylinder"></span>

All [cylinder](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **muscle** `dot`<span id="default-muscle-fpmax"></span><span id="default-muscle-vmax"></span><span id="default-muscle-lmax"></span><span id="default-muscle-lmin"></span><span id="default-muscle-scale"></span><span id="default-muscle-force"></span><span id="default-muscle-range"></span><span id="default-muscle-timeconst"></span><span id="default-muscle-interp"></span><span id="default-muscle-nsample"></span><span id="default-muscle-delay"></span><span id="default-muscle-group"></span><span id="default-muscle-user"></span><span id="default-muscle-cranklength"></span><span id="default-muscle-armature"></span><span id="default-muscle-damping"></span><span id="default-muscle-gear"></span><span id="default-muscle-forcerange"></span><span id="default-muscle-ctrlrange"></span><span id="default-muscle-forcelimited"></span><span id="default-muscle-ctrllimited"></span><span id="default-muscle"></span>

All [muscle](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

#### <span class="el-prefix">default/</span> ⁠ **adhesion** `dot`<span id="default-adhesion-nsample"></span><span id="default-adhesion-delay"></span><span id="default-adhesion-group"></span><span id="default-adhesion-user"></span><span id="default-adhesion-gain"></span><span id="default-adhesion-forcerange"></span><span id="default-adhesion-ctrlrange"></span><span id="default-adhesion-forcelimited"></span><span id="default-adhesion"></span>

All [adhesion](XMLreference.md) attributes are available here except: name, class, body.

#### <span class="el-prefix">default/</span> ⁠ **dcmotor** `dot`<span id="default-dcmotor-thermal"></span><span id="default-dcmotor-input"></span><span id="default-dcmotor-controller"></span><span id="default-dcmotor-cogging"></span><span id="default-dcmotor-inductance"></span><span id="default-dcmotor-saturation"></span><span id="default-dcmotor-nominal"></span><span id="default-dcmotor-resistance"></span><span id="default-dcmotor-motorconst"></span><span id="default-dcmotor-interp"></span><span id="default-dcmotor-nsample"></span><span id="default-dcmotor-delay"></span><span id="default-dcmotor-group"></span><span id="default-dcmotor-user"></span><span id="default-dcmotor-cranklength"></span><span id="default-dcmotor-armature"></span><span id="default-dcmotor-damping"></span><span id="default-dcmotor-gear"></span><span id="default-dcmotor-ctrlrange"></span><span id="default-dcmotor-ctrllimited"></span><span id="default-dcmotor"></span>

All [dcmotor](XMLreference.md) attributes are available here except: name, class, joint, jointinparent, site, refsite, tendon, slidersite, cranksite.

### **custom** ​

This is a grouping element for custom numeric and text elements. It does not have attributes.

#### <span class="el-prefix">custom/</span> ⁠ **numeric** ​

This element creates a custom numeric array in mjModel.


<span class="at">name</span>: <span class="at-val">string, required</span>  
The name of the array. This attribute is required because the only way to find a custom element of interest at runtime is through its name.



<span class="at">size</span>: <span class="at-val">int, optional</span>  
If specified this attribute sets the size of the data array, in doubles. If this attribute is not specified, the size will be inferred from the actual data array below.



<span class="at">data</span>: <span class="at-val">real(size), "0 0 ..."</span>  
Numeric data to be copied into mjModel. If size is specified, the length of the array given here cannot exceed the specified size. If the length of the array is smaller, the missing components are set to 0. Note that custom arrays can be created for storing information at runtime - which is why data initialization is optional. It becomes required only when the array size is omitted.


#### <span class="el-prefix">custom/</span> ⁠ **text** ​

This element creates a custom text field in mjModel. It could be used to store keyword commands for user callbacks and other custom computations.


<span class="at">name</span>: <span class="at-val">string, required</span>  
Name of the custom text field.



<span class="at">data</span>: <span class="at-val">string, optional</span>  
Custom text to be copied into mjModel. Alternatively, the text can be provided in a [CDATA section](https://www.w3.org/TR/xml/#sec-cdata-sect) of the form `<![CDATA[ ... ]]>` in the `<text>` element.


#### <span class="el-prefix">custom/</span> ⁠ **tuple** ​

This element creates a custom tuple, which is a list of MuJoCo objects. The list is created by referencing the desired objects by name.


<span class="at">name</span>: <span class="at-val">string, required</span>  
Name of the custom tuple.


##### <span class="el-prefix">tuple/</span> ⁠ **element** ​

This adds an element to the tuple.


<span class="at">objtype</span>: <span class="at-val">(any element type that can be named), required</span>  
Type of the object being added.



<span class="at">objname</span>: <span class="at-val">string, required</span>  
Name of the object being added. The type and name must reference a named MuJoCo element defined somewhere in the model. Tuples can also be referenced (including self-references).



<span class="at">prm</span>: <span class="at-val">real, "0"</span>  
Real-valued parameter associated with this element of the tuple. Its use is up to the user.


### **extension** ​

This is a grouping element for MuJoCo extensions. Extensions allow the user to extend MuJoCo's capabilities with custom code and are described in detail in the Programming chapter's [Extensions](programming/extension.md) page. Currently, the only available extension type are [Engine plugins](programming/extension.md).

#### <span class="el-prefix">extension/</span> ⁠ **plugin** ​

This element specifies that an engine plugin is required in order to simulate this model. See [Engine plugins](programming/extension.md) for more details.


<span class="at">plugin</span>: <span class="at-val">string, required</span>  
Identifier of the plugin.


##### <span class="el-prefix">plugin/</span> ⁠ **instance** ​

Declares a plugin instance. Explicit instance declaration is required when multiple elements are backed by the same plugin, or when global plugin configuration is desired. See plugin [declaration](programming/extension.md) and [configuration](programming/extension.md) for more details.


<span class="at">name</span>: <span class="at-val">string, required</span>  
Name of the plugin instance.


###### <span class="el-prefix">instance/</span> ⁠ **config** ​<span id="plugin-config"></span>

Configuration of a plugin instance. When implicitly declaring a plugin under a model element, configuration is performed with identical semantics using <span class="el">element/plugin/config</span>. The elements which currently support plugins are <span class="el">body</span>, <span class="el">flexcomp</span>, <span class="el">actuator</span> and <span class="el">sensor</span>.



<span class="at">key</span>: <span class="at-val">string, optional</span>  
Key used for plugin configuration.





<span class="at">value</span>: <span class="at-val">string, optional</span>  
Value associated with key.


