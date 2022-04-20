import { useEffect, useState } from 'react';
import parse, { domToReact, attributesToProps } from 'html-react-parser';
import { ajax } from 'rxjs/ajax';
import Tooltip from 'rc-tooltip';

const TemplateRenderer = ({ templateUrl, showTooltips = false, setOptions = () => {} }) => {
  const [html, setHtml] = useState('');
  const [opt, setOpt] = useState();

  useEffect(() => {
    setOptions(opt && JSON.parse(opt));
  }, [opt]);

  useEffect(() => {
    ajax({
      url: templateUrl,
      type: 'GET',
      responseType: 'text',
    }).subscribe(({ response }) => {
      setHtml(response);
    });
  }, [templateUrl]);

  const onLinkClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const replace = (domNode) => {
    if (domNode.type === 'style') {
      const outputString = domNode.children[0].data.replace(
        /(^(?:\s|[^@{])*?|[},]\s*)(\/\/.*\s+|.*\/\*[^*]*\*\/\s*|@media.*{\s*|@font-face.*{\s*)*([[.#]?-?[*_a-zA-Z]+[_a-zA-Z0-9-]*)(?=[^}]*{)/g,
        "$1$2 .et-template $3"
      ).replace(/(html|body)/g, ".$1");
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

    if (domNode.type === 'tag' && (domNode.name === 'body' || domNode.name === 'html')) {
      const props = attributesToProps(domNode.attribs);
      const className = props.className;
      return (
        <div {...props} className={`${domNode.name} ${className}`}>
            {domToReact(domNode.children)}
        </div>
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
