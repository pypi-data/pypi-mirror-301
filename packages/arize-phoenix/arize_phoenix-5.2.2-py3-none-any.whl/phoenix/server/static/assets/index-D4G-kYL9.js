import{j as e,w as h,aR as b,d7 as x,d8 as f,v as n,d9 as r,da as y,db as P,r as v,b as w,dc as R}from"./vendor-c0HJYYGN.js";import{v as L,a4 as z}from"./vendor-arizeai-D0FocbYu.js";import{E,L as k,R as $,r as j,a as S,F as A,A as I,b as F,c as T,P as C,h as O,M as D,d,D as B,e as M,f as N,g as q,i as G,j as W,T as K,p as H,k as c,l as J,m as Q,n as p,o as U,q as m,s as g,t as V,v as X,w as Y,x as Z,y as _,z as ee,B as re,S as ae,C as oe,G as te}from"./pages-B3HCyYqg.js";import{bo as ne,i as se,R as le,bp as ie,bq as de}from"./components-CPkaHQZs.js";import"./vendor-three-DwGkEfCM.js";import"./vendor-recharts-JMOLUxWG.js";import"./vendor-codemirror-BbCMI-_D.js";(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))i(o);new MutationObserver(o=>{for(const t of o)if(t.type==="childList")for(const l of t.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&i(l)}).observe(document,{childList:!0,subtree:!0});function u(o){const t={};return o.integrity&&(t.integrity=o.integrity),o.referrerPolicy&&(t.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?t.credentials="include":o.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function i(o){if(o.ep)return;o.ep=!0;const t=u(o);fetch(o.href,t)}})();function ce(){return e(b,{styles:a=>h`
        body {
          background-color: var(--ac-global-color-grey-75);
          color: var(--ac-global-text-color-900);
          font-family: "Roboto";
          font-size: ${a.typography.sizes.medium.fontSize}px;
          margin: 0;
          overflow: hidden;
          #root,
          #root > div[data-overlay-container="true"],
          #root > div[data-overlay-container="true"] > .ac-theme {
            height: 100vh;
          }
        }

        /* Remove list styling */
        ul {
          display: block;
          list-style-type: none;
          margin-block-start: none;
          margin-block-end: 0;
          padding-inline-start: 0;
          margin-block-start: 0;
        }

        /* A reset style for buttons */
        .button--reset {
          background: none;
          border: none;
          padding: 0;
        }
        /* this css class is added to html via modernizr @see modernizr.js */
        .no-hiddenscroll {
          /* Works on Firefox */
          * {
            scrollbar-width: thin;
            scrollbar-color: var(--ac-global-color-grey-300)
              var(--ac-global-color-grey-400);
          }

          /* Works on Chrome, Edge, and Safari */
          *::-webkit-scrollbar {
            width: 14px;
          }

          *::-webkit-scrollbar-track {
            background: var(--ac-global-color-grey-100);
          }

          *::-webkit-scrollbar-thumb {
            background-color: var(--ac-global-color-grey-75);
            border-radius: 8px;
            border: 1px solid var(--ac-global-color-grey-300);
          }
        }

        :root {
          --px-blue-color: ${a.colors.arizeBlue};

          --px-flex-gap-sm: ${a.spacing.margin4}px;
          --px-flex-gap-sm: ${a.spacing.margin8}px;

          --px-section-background-color: ${a.colors.gray500};

          /* An item is a typically something in a list */
          --px-item-background-color: ${a.colors.gray800};
          --px-item-border-color: ${a.colors.gray600};

          --px-spacing-sm: ${a.spacing.padding4}px;
          --px-spacing-med: ${a.spacing.padding8}px;
          --px-spacing-lg: ${a.spacing.padding16}px;

          --px-border-radius-med: ${a.borderRadius.medium}px;

          --px-font-size-sm: ${a.typography.sizes.small.fontSize}px;
          --px-font-size-med: ${a.typography.sizes.medium.fontSize}px;
          --px-font-size-lg: ${a.typography.sizes.large.fontSize}px;

          --px-gradient-bar-height: 8px;

          --px-nav-collapsed-width: 45px;
          --px-nav-expanded-width: 200px;
        }

        .ac-theme--dark {
          --px-primary-color: #9efcfd;
          --px-primary-color--transparent: rgb(158, 252, 253, 0.2);
          --px-reference-color: #baa1f9;
          --px-reference-color--transparent: #baa1f982;
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
        .ac-theme--light {
          --px-primary-color: #00add0;
          --px-primary-color--transparent: rgba(0, 173, 208, 0.2);
          --px-reference-color: #4500d9;
          --px-reference-color--transparent: rgba(69, 0, 217, 0.2);
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
      `})}const pe=x(f(n(r,{path:"/",errorElement:e(E,{}),children:[e(r,{path:"/login",element:e(k,{})}),e(r,{path:"/reset-password",element:e($,{}),loader:j}),e(r,{path:"/reset-password-with-token",element:e(S,{})}),e(r,{path:"/forgot-password",element:e(A,{})}),e(r,{element:e(I,{}),loader:F,children:n(r,{element:e(T,{}),children:[e(r,{path:"/profile",handle:{crumb:()=>"profile"},element:e(C,{})}),e(r,{index:!0,loader:O}),n(r,{path:"/model",handle:{crumb:()=>"model"},element:e(D,{}),children:[e(r,{index:!0,element:e(d,{})}),e(r,{element:e(d,{}),children:e(r,{path:"dimensions",children:e(r,{path:":dimensionId",element:e(B,{}),loader:M})})}),e(r,{path:"embeddings",children:e(r,{path:":embeddingDimensionId",element:e(N,{}),loader:q,handle:{crumb:a=>a.embedding.name}})})]}),n(r,{path:"/projects",handle:{crumb:()=>"projects"},element:e(G,{}),children:[e(r,{index:!0,element:e(W,{})}),n(r,{path:":projectId",element:e(K,{}),loader:H,handle:{crumb:a=>a.project.name},children:[e(r,{index:!0,element:e(c,{})}),e(r,{element:e(c,{}),children:e(r,{path:"traces/:traceId",element:e(J,{})})})]})]}),n(r,{path:"/datasets",handle:{crumb:()=>"datasets"},children:[e(r,{index:!0,element:e(Q,{})}),n(r,{path:":datasetId",loader:p,handle:{crumb:a=>a.dataset.name},children:[n(r,{element:e(U,{}),loader:p,children:[e(r,{index:!0,element:e(m,{}),loader:g}),e(r,{path:"experiments",element:e(m,{}),loader:g}),e(r,{path:"examples",element:e(V,{}),loader:X,children:e(r,{path:":exampleId",element:e(Y,{})})})]}),e(r,{path:"compare",handle:{crumb:()=>"compare"},loader:Z,element:e(_,{})})]})]}),e(r,{path:"/playground",element:e(ee,{}),handle:{crumb:()=>"Playground"}}),e(r,{path:"/apis",element:e(re,{}),handle:{crumb:()=>"APIs"}}),e(r,{path:"/settings",element:e(ae,{}),handle:{crumb:()=>"Settings"}})]})})]})),{basename:window.Config.basename});function me(){return e(y,{router:pe})}function ge(){return e(oe,{children:e(ne,{children:e(ue,{})})})}function ue(){const{theme:a}=se();return e(z,{theme:a,children:e(P,{theme:L,children:n(w.RelayEnvironmentProvider,{environment:le,children:[e(ce,{}),e(te,{children:e(ie,{children:e(v.Suspense,{children:e(de,{children:e(me,{})})})})})]})})})}const he=document.getElementById("root"),be=R.createRoot(he);be.render(e(ge,{}));
