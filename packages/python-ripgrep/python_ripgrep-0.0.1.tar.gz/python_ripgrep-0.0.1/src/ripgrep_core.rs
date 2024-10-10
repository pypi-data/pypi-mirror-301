use std::{borrow::BorrowMut, ffi::{OsStr, OsString}};
use hiargs::HiArgs;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

mod search;
mod hiargs;
mod lowargs;
mod haystack;
#[macro_use]
mod messages;


#[pyclass]
pub struct PyArgs {
    pub patterns: Vec<String>,
    pub paths: Option<Vec<String>>,
    pub globs: Option<Vec<String>>,
    pub heading: Option<bool>,
    pub separator_field_context: Option<String>,
    pub separator_field_match: Option<String>,
    pub separator_context: Option<String>,
    pub sort: Option<PySortMode>,
    pub max_count: Option<u64>,
}

#[pymethods]
impl PyArgs {
    #[new]
    #[pyo3(signature = (
        patterns, 
        paths=None, 
        globs=None, 
        heading=None, 
        separator_field_context=None, 
        separator_field_match=None, 
        separator_context=None,
        sort=None,
        max_count=None,
    ))]
    fn new(
        patterns: Vec<String>, 
        paths: Option<Vec<String>>, 
        globs: Option<Vec<String>>,
        heading: Option<bool>,
        separator_field_context: Option<String>,
        separator_field_match: Option<String>,
        separator_context: Option<String>,
        sort: Option<PySortMode>,
        max_count: Option<u64>,
    ) -> Self {
        PyArgs {
            patterns,
            paths,
            globs,
            heading,
            separator_field_context,
            separator_field_match,
            separator_context,
            sort,
            max_count,
        }
    }
}


#[pyclass(eq)]
#[derive(PartialEq, Clone)]
#[pyo3(get_all)]
pub struct PySortMode {
    pub kind: PySortModeKind,
    pub reverse: bool,
}

#[pymethods]
impl PySortMode {
    #[new]
    #[pyo3(signature = (kind, reverse=false))]
    fn new(
        kind: PySortModeKind,
        reverse: bool,
    ) -> Self {
        PySortMode {
            kind,
            reverse,
        }
    }
}


#[pyclass(eq)]
#[derive(PartialEq, Clone)]
#[pyo3(get_all)]
pub enum PySortModeKind {
    Path,
    LastModified,
    LastAccessed,
    Created,
}

fn build_patterns(patterns: Vec<String>) -> Vec<lowargs::PatternSource> {
    patterns.into_iter().map(|pattern| lowargs::PatternSource::Regexp(pattern)).collect()
}

fn build_paths(paths: Vec<String>) -> Vec<OsString> {
    paths.into_iter().map(|path| OsString::from(path)).collect()
}


fn build_sort_mode_kind(kind: PySortModeKind) -> lowargs::SortModeKind {
    match kind {
        PySortModeKind::Path => lowargs::SortModeKind::Path,
        PySortModeKind::LastModified => lowargs::SortModeKind::LastModified,
        PySortModeKind::LastAccessed => lowargs::SortModeKind::LastAccessed,
        PySortModeKind::Created => lowargs::SortModeKind::Created,
    }
}

fn build_sort_mode(sort: Option<PySortMode>) -> Option<lowargs::SortMode> {
    if let Some(sort_mode) = sort {
        Some(lowargs::SortMode { kind: build_sort_mode_kind(sort_mode.kind), reverse: sort_mode.reverse })
    } else {
        None
    }
}

fn pyargs_to_hiargs(py_args: &PyArgs, mode: lowargs::Mode) -> anyhow::Result<HiArgs> {
    let mut low_args = lowargs::LowArgs::default();

    low_args.patterns = build_patterns(py_args.patterns.clone());

    low_args.mode = mode;

    low_args.sort = build_sort_mode(py_args.sort.clone());

    low_args.heading = py_args.heading;

    low_args.max_count = py_args.max_count;

    if let Some(globs) = &py_args.globs {
        low_args.globs = globs.clone();
    }

    if let Some(paths) = &py_args.paths {
        low_args.positional = build_paths(paths.clone());
    }

    if let Some(separator_field_context) = &py_args.separator_field_context {
        let sep = OsStr::new(separator_field_context);
        low_args.field_context_separator = lowargs::FieldContextSeparator::new(&sep).unwrap();
    }

    if let Some(separator_field_match) = &py_args.separator_field_match {
        let sep = OsStr::new(separator_field_match);
        low_args.field_match_separator = lowargs::FieldMatchSeparator::new(&sep).unwrap();
    }

    if let Some(separator_context) = &py_args.separator_context {
        let sep = OsStr::new(separator_context);
        low_args.context_separator = lowargs::ContextSeparator::new(&sep).unwrap();
    }

    HiArgs::from_low_args(low_args)
}


#[pyfunction]
#[pyo3(name = "search")]
pub fn py_search(py_args: &PyArgs) -> PyResult<Vec<String>> {
    let args_result = pyargs_to_hiargs(py_args, lowargs::Mode::default());

    if let Err(err) = args_result {
        return Err(PyValueError::new_err(err.to_string()));
    }
    
    let args = args_result.unwrap();

    let search_result = py_search_impl(&args);

    if let Err(err) = search_result {
        return Err(PyValueError::new_err(err.to_string()));
    }

    Ok(search_result.unwrap())
}



fn py_search_impl(args: &HiArgs) -> anyhow::Result<Vec<String>> {
    let haystack_builder = args.haystack_builder();
    let unsorted = args
        .walk_builder()?
        .build()
        .filter_map(|result| haystack_builder.build_from_result(result));
    let haystacks = args.sort(unsorted);

    let args_matcher = args.matcher()?;
    let args_searcher = args.searcher()?;
    let args_printer = args.printer_no_color(vec![]);

    let mut results = Vec::new();

    let mut searcher = args.search_worker(
        args_matcher,
        args_searcher,
        args_printer,
    )?;

    for haystack in haystacks {
        let search_result = match searcher.search(&haystack) {
            Ok(search_result) => search_result,
            // A broken pipe means graceful termination.
            Err(err) if err.kind() == std::io::ErrorKind::BrokenPipe => break,
            Err(err) => {
                err_message!("{}: {}", haystack.path().display(), err);
                continue;
            }
        };

        if search_result.has_match() {     
            let printer = searcher.printer();
            let results_vec = printer.get_mut().borrow_mut();
            let results_str = String::from_utf8(results_vec.get_ref().clone()).unwrap();
            results.push(results_str.clone());

            let p = searcher.printer().borrow_mut();
            let p_inner = p.get_mut();
            p_inner.get_mut().clear();
        }
    }

    Ok(results)
}


#[pyfunction]
#[pyo3(name = "files")]
pub fn py_files(py_args: &PyArgs) -> PyResult<Vec<String>> {
    let args_result = pyargs_to_hiargs(py_args, lowargs::Mode::Files);

    if let Err(err) = args_result {
        return Err(PyValueError::new_err(err.to_string()));
    }
    
    let args = args_result.unwrap();

    let files_result = py_files_impl(&args);

    if let Err(err) = files_result {
        return Err(PyValueError::new_err(err.to_string()));
    }

    Ok(files_result.unwrap())
}


fn py_files_impl(args: &HiArgs) -> anyhow::Result<Vec<String>> {
    let haystack_builder = args.haystack_builder();
    let walk_builder = args.walk_builder()?;

    let unsorted = walk_builder
        .build()
        .filter_map(|result| haystack_builder.build_from_result(result));

    let haystacks = args.sort(unsorted);

    let mut matches = Vec::new();

    for haystack in haystacks {
        if args.quit_after_match() {
            break;
        }

        if let Some(max_count) = args.max_count() {
            if matches.len() >= max_count as usize {
                break;
            }
        }

        let haystack_path = haystack
            .path()
            .to_str();

        if let Some(path) = haystack_path {
            matches.push(path.to_string());
        }
    }

    Ok(matches)
}