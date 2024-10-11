/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/





class IdeTesterGuiManager extends IdeRunner {

  constructor(editorId){
    super(editorId)
    this.delay       = 0     // Override: no pause when starting the executions
    this.conf        = null
    this.testing     = false
    this.toSwap      = [this.data, this.getCodeToTest] // nothing to swap...
    this.ides_cache  = {}
    this.test_cases  = []   // Linearized version of CASES_DATA
    this.std_capture = []   // Full stdout+stdErr capture, BEFORE any jQuery.terminal formatting
    this.counters    = {skip:0, remaining:0, failed:0, success:0}
  }


  // @Override
  checkSrcHash(){}


  // @Override
  build(){
    super.build()

    const confsArr = Object.values(CASES_DATA)
    confsArr.forEach( this.setupOneConfCaseAndAllSubcases.bind(this) )
    this.finalizeGlobalUiAndCounters(confsArr.length, this.test_cases.length)
  }



  finalizeGlobalUiAndCounters(nIdes, nTests){

    // configure "run all" button:
    $(this.globalIdH).parent()
                     .find('button[btn_kind=test_ides]')
                     .on('click', ()=>this.runAllTests())

    // Configure global buttons (select-all, unselect-all):
    ;[ [false, ''], [true, 'un'] ].forEach(([state,prefix])=>{
      $(`button#${ prefix }select-all`).on('click', _=>{
        this.test_cases.forEach(o=>{
          o.skip = state
          this.setSvgAndCounters(o, prefix+'checked')
        })
        this.displayCounters()
      })
    })

    // Configure 'human" global button:
    $(`button#toggle-human`).on('click', _=>{
      this.test_cases.forEach(o=>{
        if(!o.human) return;
        o.skip = !o.skip
        this.setSvgAndCounters(o, `${ o.skip?'un':'' }checked`)
      })
      this.displayCounters()
    })

    // Finalize and display initial counters state, once all the tests have been registered:
    const allHtml = nTests==nIdes ? nIdes : `${ nIdes }<br>(${ nTests } cases)`
    $('#cnt-all').html(allHtml)
    this.displayCounters()
  }



  setupOneConfCaseAndAllSubcases(conf){
    const batchOfTests = []

    if(!conf.subcases){
      // Simple case (one test only):
      this.registerOneTestAndSetupUI(conf, batchOfTests)

    }else{
      // If subcases are defined:
      const propsToReport = 'editor_id ide_link ide_name page_url rel_dir_url'.split(' ')
      conf.subcases.forEach( (subConf, i)=>{
        if(i) subConf.no_clear = true            // Keep original choice for first only
        for(const prop of propsToReport){
          subConf[prop] = conf[prop]
        }
        this.registerOneTestAndSetupUI(subConf, batchOfTests, i+1)

        // Bind subcases "play" buttons: "run all subcases until this one"
        $(`#play${i+1}-${ conf.editor_id } > button`).on(
          'click', ((testsUpTo)=> ()=>this.runAllTests(testsUpTo) )(batchOfTests.slice())
        )
      })
    }

    // Bind the top level case buttons:
    $(`#test-btns-${ conf.editor_id } > button[btn_kind=test_1_ide]`).on(
      'click', ()=>this.runAllTests(batchOfTests)
    )
    $(`#test-btns-${ conf.editor_id } > button[btn_kind=load_ide]`).on(
      'click', this.loadFactory(conf)
    )
  }



  registerOneTestAndSetupUI(conf, batchOfTests, tailId=""){

    this.test_cases.push(conf)
    batchOfTests.push(conf)

    this.testConfStandardization(conf, tailId)

    const [countProp, setupClass] = conf.skip ? ['skip','unchecked'] : ['remaining','checked']
    this.counters[countProp]++

    $(conf.divSvgBtnsId)
      .html(CONFIG.QCM_SVG)
      .addClass([ 'multi', setupClass])
      .on( 'click', _=>{
          if(this.testing) return;
          this.setSvgAndCounters(conf, conf.skip ? 'checked':'unchecked')
          this.displayCounters()
      })
  }



  /**Initial conversion steps, to finalize the python->JS transfer of the tests data.
   * */
  testConfStandardization(conf, tailId){

    conf.divSvgBtnsId = `#status${ tailId }-${ conf.editor_id }`

    conf.fail = Boolean( conf.fail || conf.in_error_msg || conf.not_in_error_msg )
    conf.skip = Boolean( conf.skip || conf.human )

    // `reveal_corr_rems:undefined` means this won't be tested:
    if('reveal_corr_rems' in conf){
      conf.reveal_corr_rems = Boolean(conf.reveal_corr_rems)
    }
    // Initialize the test state flag (to know if it has been done in the tests or not):
    conf.revealedCorrRems = false

    ;'std_capture_regex not_std_capture_regex'.split(' ').forEach( prop=>{
      if(conf[prop]) conf[prop] = new RegExp(conf[prop], 's')
    })

    conf.assertions = !conf.assertions ? [] : conf.assertions.split(' ').map(rule=>{
      const prop=rule.replace(/^!/, '')
      const revExpected = rule.startsWith('!')  // Reversing to enforce booleans everywhere
      return (obj) => !obj[prop]==revExpected ? "" : `${ prop }: should be ${ !revExpected }`
    })
  }



  /**Update the html class of the svg container with the given id.
   * */
  setSvgAndCounters(conf, kls){
    const div = $(conf.divSvgBtnsId)
    this.updateCountersFor(div, -1)
    div.removeClass(['checked', 'unchecked', 'correct', 'incorrect', 'must-fail'])
    div.addClass(kls)
    this.updateCountersFor(div, +1)
    conf.skip = div.hasClass('unchecked')
  }


  updateCountersFor(div, delta){
    if(div.hasClass('correct'))   this.counters.success   += delta
    if(div.hasClass('incorrect')) this.counters.failed    += delta
    if(div.hasClass('checked'))   this.counters.remaining += delta
    if(div.hasClass('unchecked')) this.counters.skip      += delta
  }


  /**Update the values of each counter.
   * */
  displayCounters(){
    Object.entries(this.counters).forEach( ([cnt,n])=>{ $('#cnt-'+cnt).text(n) })
  }


  // Override
  terminalEcho(content, options){
    this.std_capture.push(content)
    super.terminalEcho(content, options)
  }


  swapConfAndData(){
    ;[this.data, this.toSwap[0]]          = [this.toSwap[0], this.data]
    ;[this.getCodeToTest, this.toSwap[1]] = [this.toSwap[1], this.getCodeToTest]
  }


  // Override
  terminalDisplayOnStart(){
    if(this.isTesting()){
      this.terminal.echo(`Testing: ${ this.conf.ide_name }`)
    }
    super.terminalDisplayOnStart()
  }





  /**Runtime to apply when clicking on a button to "download" all the code of an
   * IDE in the testing one.
   * */
  loadFactory(conf){
    return async ()=>{
      await waitForPyodideReady()

      if(this.testing) return;    // Deactivated during tests (otherwise, big troubles...)

      this.data = await this.getIdeData(conf)   // Update first (see getters)

      const sections = [
        this._toSection('env',       this.envContent),
        this._toSection('env_term',  this.envTermContent),
        this._toSection('corr',      this.corrContent),
        this._toSection('code',      this.userContent),
        this._toSection('post_term', this.postTermContent),
        this._toSection('post',      this.postContent),
      ]
      const codeToTest = sections.splice( 2+Boolean(conf.code), 1)[0]

      const fullCode = [
        codeToTest,
        CONFIG.lang.tests.msg.trimEnd(),
        this._toSection('tests', this.publicTests),
        this._toSection('secrets', this.secretTests),
        `\n\n"""\n${ sections.join('').replace(/"""/g, '\\"\\"\\"').trimStart() }\n"""`
      ].join('')

      this.applyCodeToEditorAndSave(fullCode)
    }
  }



  /**Build a sub section of the original python file.
   * */
  _toSection(py_section, content){
    return content && `\n\n# --- PYODIDE:${ py_section } --- #\n${ content }`
  }




  save(_){}

  runAllTests(){ throw new Error('Not implemented') }

  /**Is the current action "running all IDEs tests"? (or even, only some of them...)
   * */
  isTesting(){ return this.running.includes(CONFIG.running.testing) }



  /**Extract the config object for the given IDE, getting rid of the profile data on the way.
   * Data are cached so that a page is requested once only.
   * @returns a copy of the original object (so that it can be modified on the fly by the caller)
   * */
  async getIdeData(conf){

    // Request + store the data for all the IDEs in the related page, if missing:
    if(!this.ides_cache[conf.editor_id]){

      const response = await fetch(conf.page_url)
      const html     = await response.text()

      const reg      = /(?<=PAGE_IDES_CONFIG\s*=\s*['"]).+?(?=["']\s*<\/script>)/
      const compress = html.match(reg)[0]                 // Does always match!
      const fix_comp = compress.replace(/\\x1e/g, "\x1e")
      const configs  = decompressAndConvert(fix_comp)

      Object.entries(configs).forEach( ([editor,data])=>{
        conf._profile = data.profile
        if(!conf.keep_profile) data.profile = null   // Remove profile info for tests (by default).
        this.ides_cache[editor] = this._prepareData(data)
      })
    }

    // Extract ide's data object, enforcing its existence:
    const data = this.ides_cache[conf.editor_id]

    if(!data) throw new Error(
      `Couldn't extract data for ${ conf.ide_name }.\nIf this is an IDE without python file, `
      +"you should restart mkdocs serve (the ids generator is now out of synch with the "
      +"rendered data). Otherwise, please raise an issue on the project's repository."
    )

    // Send back a copy, to allow runtime mutation while keeping a clean initial state
    return {...data}
  }
}














class IdeTester extends IdeTesterGuiManager {



  async runAllTests(targets){
    if(this.testing) return;
    await waitForPyodideReady()

    this.terminal.clear()
    const start = Date.now()
    this.testing = true

    const confsToRun = (targets ?? this.test_cases).filter( conf =>{
      const skip = (!targets || targets.length!=1) && conf.skip
      if(!skip){
        this.setSvgAndCounters(conf, 'checked')
      }
      return !skip
    })

    this.displayCounters()

    const final = (isOk)=>(arg)=>{
      this.testing  = false
      const txt     = isOk ? CONFIG.lang.testsDone.msg : txtFormat.error(String(arg))
      const elapsed = ((Date.now() - start) / 1000).toFixed(1)

      this.terminal.echo(txt)
      this.terminal.echo(txtFormat.info(`(Elapsed time: ${ elapsed }s)`))
    }

    /* Running everything in order: it's actually a bit faster (probably because not queueing again
       and again while waiting in getIdeData...?). So don't bother with Promise.all anymore...  */
    try{
      for(const conf of confsToRun){
        this.conf = conf
        jsLogger('[Testing] - start', conf.ide_name)
        if(conf.run_play){
          await this.playFactory(CONFIG.running.testingPlay)()
        }else{
          await this.validateFactory(CONFIG.running.testingValid)()
        }
        jsLogger('[Testing] - done', conf.ide_name)
      }
      final(true)()
    }catch{
      final(false)()
    }
  }



  buildCodeGetter(){
    const cbk = this.conf.code ? ()=>this.userContent : ()=>this.corrContent
    if(this.conf.run_play){
      return ()=>this._joinCodeAndPublicSections(cbk())
    }
    return cbk
  }


  // @Override
  setAttemptsCounter(n, low=false){
    n = Number.isFinite(n) ? n : "∞"
    if(low){
      $(this.counterH+'-low').text(n)
    }
    super.setAttemptsCounter(n)
  }




  // @Override
  async setupRuntimeIDE(){

    if(this.isTesting()){
      const data = await this.getIdeData(this.conf)

      ;`decrease_attempts_on_user_code_failure
        deactivate_stdout_for_secrets
        show_only_assertion_errors_for_secrets
      `.trim()
        .split(/\s+/).forEach(prop=>{
        if(prop in this.conf) data[prop] = this.conf[prop]
      })

      this.toSwap = [ data, this.buildCodeGetter() ]
      this.swapConfAndData()

      if('set_max_and_hide' in this.conf){
        const max = this.conf.set_max_and_hide==1000 ? Infinity : this.conf.set_max_and_hide
        this.data.attempts_left = max
        this.hiddenDivContent   = true
        this.conf.revealedCorrRems = false
      }
      this.setAttemptsCounter(this.attemptsLeft, true)
      this.conf.attempts_start = this.attemptsLeft

      this.terminal.settings().outputLimit = this.stdoutCutOff
      this.updateStdoutCutFeedback(this.cutFeedback)

      pyodide.runPython(pyodideFeatureCode('refresher'))
      // Do NOT clear the scope in teardownRuntime: would forbid playing with the terminal afterward.
      if(!this.conf.no_clear){
        pyodide.runPython('clear_scope()')
        this._ide_init()
      }
      this.setupFetchers(this.conf)
    }

    return await super.setupRuntimeIDE()
  }



  // @Override
  async teardownRuntimeIDE(runtime){
    try{
      await super.teardownRuntimeIDE(runtime)

    }finally{
      if(!this.isTesting()) return;

      this.conf.attempts_end = this.attemptsLeft  // Store before swap
      const testOutcome = this._analyzeTestOutcome(runtime)

      const success     = !testOutcome
      const classToBe   = !success        ? 'incorrect'
                        : !this.conf.fail ? 'correct'
                                          : ['correct','must-fail']
                                                        // warning: .must-fail always last!

      this.swapConfAndData()    // Has to always occur
      this.teardownFetchers()   // Has to always occur

      this.setSvgAndCounters(this.conf, classToBe)
      this.displayCounters()
      this.std_capture.length = 0   // Always...

      if(testOutcome){
        if(!runtime) throw new Error(testOutcome)
        else         console.error(testOutcome)
      }
    }
  }


  // Override
  revealSolutionAndRems(){
    this.conf.revealedCorrRems = true
    this.hiddenDivContent = false      // Mimic actual behavior
  }



  _analyzeTestOutcome(runtime){
    if(!runtime) return "Probably failed in the env section..."

    const fullOut = this.std_capture.join('\n')
    let msg = []

    if(!Number.isFinite(this.conf.attempts_start)){
      if(Number.isFinite(this.conf.attempts_end)) msg.push(
        "The number of attempts left should still be infinite, but was: " + this.conf.attempts_end
      )
    }else if(this.conf.delta_attempts!==undefined){
      const actual = this.conf.attempts_end - this.conf.attempts_start
      const exp    = this.conf.delta_attempts
      if(exp != actual) msg.push(
        `Delta attempts: ${ actual } should be ${ exp }`
      )
    }

    if( ('reveal_corr_rems' in this.conf)){
      if(this.conf.reveal_corr_rems !== this.conf.revealedCorrRems) msg.push(
        this.conf.reveal_corr_rems ? "Corr/REMs should have been revealed."
                                   : "Corr/REMs should NOT have been revealed."
      )
    }

    const assertions=this.conf.assertions.map(check=>check(this)).join('')
    if(assertions) msg.push(assertions)

    if(this.conf.in_error_msg && !runtime.stdErr.includes(this.conf.in_error_msg)){
      msg.push(`The error message should contain; "${this.conf.in_error_msg}"`)
    }

    if(this.conf.not_in_error_msg && runtime.stdErr.includes(this.conf.not_in_error_msg)){
      msg.push(`The error message should NOT contain; "${this.conf.not_in_error_msg}"`)
    }

    if(this.conf.std_capture_regex && !this.conf.std_capture_regex.test(fullOut) ){
      msg.push("The std output/error should match " + this.conf.std_capture_regex)
    }

    if(this.conf.not_std_capture_regex && this.conf.not_std_capture_regex.test(fullOut) ){
      msg.push("The std output/error should NOT match " + this.conf.not_std_capture_regex)
    }

    if(!msg.length && runtime.stopped === this.conf.fail){
      return ""
    }

    msg = [
      `Test failed for ${this.conf.ide_link} :`,
      runtime.stdErr || "No error raised, but...",
      ...msg
    ]
    return msg.join('\n\n')
  }



  /**Setup the pyodide environment so that requests to relative urls are automatically redirected
   * to the correct (original) locations, and setup various sinks to avoids DOM interactions to
   * fail, typically when trying to update img tags through `PyodidePlot` or `mermaid_figure`.
   * */
  setupFetchers(conf){

    CONFIG.relUrlRedirect = `${ CONFIG.baseUrl }/${ conf.rel_dir_url }/`.replace(/[/]{2}/g, '/')

    pyodide.runPython(`

def __hack_pyfetch():
    import re, js
    from functools import wraps
    import pyodide.http as http

    pure_pyfetch = http.pyfetch
    pure_import  = __import__


    @wraps(pure_pyfetch)
    async def pyfetch(url, *a, **kw):
        if isinstance(url,str) and not re.match(r'(https?|ftps?|file)://|www[.]', url):
            url = js.config().relUrlRedirect + url
        return await pure_pyfetch(url, *a, **kw)
    http.pyfetch = pyfetch


    async def fake_fetch(url, *a):
        if isinstance(url,str) and not re.match(r'(https?|ftps?|file)://|www[.]', url):
            url = js.config().relUrlRedirect + url
        return await js.fetch(url, *a)


    class JsMock(int):
        """ Extends int so that computations when pyplot tries to update the DOM do not
            crash (even if wrong)
        """

        # ASYNC_CALLS = set('uploaderAsync'.split())

        def __getattr__(self, k):
            if k=='fetch':  return fake_fetch

            # if k in self.ASYNC_CALLS:  return self.async_sink_js

            if self is sink_js or k in ('document',):
                return sink_js
            return getattr(js,k)

        async def async_sink_js(self, *a,**kw):
            return sink_js

        def __call__(self, *a, **kw):
            return sink_js

        def __setattr__(self, k,v):
            setattr(js, k, v)

    fake_js = JsMock(1)
    sink_js = JsMock(1)  # HAS to be another instance than fake_js!

    def fake_import(name, *a, **kw):
        if name == 'js':
            return fake_js
        return pure_import(name, *a, **kw)
    __builtins__.__import__ = fake_import


    def teardown_tests():
        http.pyfetch = pure_pyfetch
        __builtins__.__import__ = pure_import
    __builtins__.teardown_tests = teardown_tests


__hack_pyfetch()
del __hack_pyfetch`)
  }


  teardownFetchers(){
    CONFIG.relUrlRedirect = ''
    pyodide.runPython("teardown_tests()")
  }
}


CONFIG.CLASSES_POOL.IdeTester = IdeTester
