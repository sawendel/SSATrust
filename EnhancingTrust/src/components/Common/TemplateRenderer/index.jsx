import { useMemo, useEffect, useState } from 'react';
import parse, { domToReact, attributesToProps } from 'html-react-parser';
import { ajax } from 'rxjs/ajax';
import Tooltip from 'rc-tooltip';
import { toast } from 'react-toastify';
import { Events } from '../../../constants';
import Overlay from '../Overlay';

const TemplateRenderer = ({
  templateUrl,
  mobileTemplate,
  showTooltips = false,
  options,
  logEvent,
  setOptions = () => { } },
) => {
  const [showOverlay, setShowOverlay] = useState(false);
  const [html, setHtml] = useState('');
  const [opt, setOpt] = useState();
  const template = useMemo(() => window.innerWidth < 768 && mobileTemplate
    ? mobileTemplate : templateUrl, [mobileTemplate, templateUrl]);

  useEffect(() => {
    setOptions(opt && JSON.parse(opt));
  }, [opt]);

  useEffect(() => {
    ajax({
      url: template,
      type: 'GET',
      responseType: 'text',
    }).subscribe(({ response }) => {
      setHtml(response);
    });
  }, [template]);

  const eventHandler = (e, event, attribs, metadata) => {
    if (typeof attribs?.['data-default'] === 'undefined') {
      e.preventDefault();
      e.stopPropagation();
    }

    logEvent(event, metadata);
  };

  const onLinkClick = (...params) => {
    eventHandler(...params);
    toast.info("All links have been disabled in this study", {
      onClose: () => setShowOverlay(false),
      onOpen: () => setShowOverlay(true),
    });
    toast.clearWaitingQueue();
  }

  const replace = (domNode) => {
    if (domNode.type === 'style' && domNode.children?.[0]?.data) {
      const outputString = domNode.children[0].data.replace(
        /(^(?:\s|[^@{])*?|[},]\s*)(\/\/.*\s+|.*\/\*[^*]*\*\/\s*|@media.*{\s*|@font-face.*{\s*)*([[.#]?-?[*_a-zA-Z]+[_a-zA-Z0-9-]*)(?=[^}]*{)/g,
        "$1$2 .et-template $3"
      ).replace(/[\s\}](html|body)/g, " .$1");
      domNode.children[0].data = outputString;
    }

    if (domNode.type === 'script') {
      if (typeof domNode.attribs?.['data-config'] !== 'undefined' && domNode?.children?.[0]?.data) {
        // eslint-disable-next-line no-eval
        const config = eval(domNode.children[0].data);
        if (opt !== JSON.stringify(config)) {
          setOpt(JSON.stringify(config));
        }
      }
      return <></>;
    }

    if (domNode.attribs?.['data-tooltip'] && showTooltips) {
      const props = attributesToProps(domNode.attribs);
      const Tag = domNode.name;
      return (
        <>
          <Tooltip placement="top" visible overlay={<> <i className="et-warning" />  <span dangerouslySetInnerHTML={{ __html: '<span>' + domNode.attribs?.['data-tooltip'] + '</span> ' }} /> </>}>
            <Tag {...props}>
              {domToReact(domNode.children)}
            </Tag>
          </Tooltip>
        </>
      );
    }

    if (domNode.name === 'link' && domNode.attribs.rel === 'stylesheet') {
      return <></>
    }

    if (domNode.type === 'tag' && domNode.name === 'button') {
      const props = attributesToProps(domNode.attribs);
      const logData = domNode.attribs['aria-label'] || domNode.attribs.name || domNode.children[domNode.children.length - 1].data.trim();
      return (
        <button {...props} onClick={(e) => eventHandler(e, Events.BUTTON_CLICKED, domNode.attribs, logData)}>
          {domToReact(domNode.children)}
        </button>
      )
    }

    if (domNode.type === 'tag' && domNode.name === 'a') {
      const props = attributesToProps(domNode.attribs);
      const { href } = domNode.attribs;
      let updatedHref = href;
      if (href && options?.url && !href.startsWith('http')) {
        updatedHref = `${options.url.replace(/\/$/, '')}/${href.replace(/^\//, '')}`;
      }
      return (
        <a {...props} href={updatedHref} onClick={(e) => onLinkClick(e, Events.LINK_CLICKED, undefined, updatedHref)} title={updatedHref}>
          {domToReact(domNode.children)}
        </a>
      )
    }

    if (domNode.type === 'tag' && domNode.name === 'form') {
      const props = attributesToProps(domNode.attribs);
      return (
        <form {...props} onSubmit={(e) => eventHandler(e, Events.FORM_SUBMITTED)}>
          {domToReact(domNode.children, {replace})}
        </form>
      )
    }
  }

  return (
    <>
      {showOverlay && <Overlay onClick={() => toast.dismiss()} />}
      <div className="et-template">
        {parse(html, { replace })}
      </div>
    </>
  )
};

export default TemplateRenderer;
