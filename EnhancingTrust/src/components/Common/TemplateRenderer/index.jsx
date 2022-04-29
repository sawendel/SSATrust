import { useMemo, useEffect, useState } from 'react';
import parse, { domToReact, attributesToProps } from 'html-react-parser';
import { ajax } from 'rxjs/ajax';
import Tooltip from 'rc-tooltip';

const TemplateRenderer = ({ templateUrl, mobileTemplate, showTooltips = false, setOptions = () => {} }) => {
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

  const onLinkClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const onSubmitClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

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
          <Tooltip placement="top" visible overlay={<><i className="et-warning" /> {domNode.attribs?.['data-tooltip']}</>}>
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

    if (domNode.type === 'tag' && domNode.name === 'a') {
      const props = attributesToProps(domNode.attribs);
      const { href } = domNode.attribs;
      return (
        <a {...props} href={href} onClick={onLinkClick} title={href}>
            {domToReact(domNode.children)}
        </a>
      )
    }

    if (domNode.type === 'tag' && domNode.name === 'form') {
      const props = attributesToProps(domNode.attribs);
      return (
        <form {...props} onSubmit={onSubmitClick}>
          {domToReact(domNode.children)}
        </form>
      )
    }
  }

  return (
    <div className="et-template">
      {parse(html, { replace })}
    </div>
  )
};

export default TemplateRenderer;
