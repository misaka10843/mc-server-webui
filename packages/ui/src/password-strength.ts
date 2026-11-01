let engine: Promise<import('@zxcvbn-ts/core').ZxcvbnFactory> | undefined
export const loadPasswordEstimator = () => {
  engine ??= Promise.all([import('@zxcvbn-ts/core'), import('@zxcvbn-ts/language-common'), import('@zxcvbn-ts/language-en')]).then(([core, common, english]) => new core.ZxcvbnFactory({
    translations: english.translations,
    graphs: common.adjacencyGraphs,
    dictionary: { ...common.dictionary, ...english.dictionary },
  })).catch(cause => { engine = undefined; throw cause })
  return engine
}
